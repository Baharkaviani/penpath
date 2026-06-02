from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ScanUpload, Week
from .serializers import (
    MeSerializer,
    ScanUploadSerializer,
    UserBadgeSerializer,
    WeekDetailSerializer,
    WeekListSerializer,
    WeekWriteSerializer,
    build_dashboard_payload,
)
from .services import close_week
from .tasks import process_scan
from .week_factory import ensure_current_week


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(MeSerializer(request.user).data)


class CsrfView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({'csrfToken': get_token(request)})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')
        if not username or not password:
            return Response({'detail': 'Username and password required.'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Username taken.'}, status=400)
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return Response(MeSerializer(user).data, status=201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get('username', ''),
            password=request.data.get('password', ''),
        )
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=400)
        login(request, user)
        return Response(MeSerializer(user).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out.'})


class WeekListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WeekListSerializer

    def get_queryset(self):
        return Week.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CurrentWeekView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        week = ensure_current_week(request.user)
        return Response(WeekDetailSerializer(week).data)

    def patch(self, request):
        week = ensure_current_week(request.user)
        if week.is_closed:
            return Response({'detail': 'Week is closed.'}, status=400)
        writer = WeekWriteSerializer()
        week = writer.update_week(week, request.data)
        return Response(WeekDetailSerializer(week).data)


class WeekDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_week(self, request, week_id):
        return get_object_or_404(Week, user=request.user, start_date=week_id)

    def get(self, request, week_id):
        week = self.get_week(request, week_id)
        return Response(WeekDetailSerializer(week).data)

    def patch(self, request, week_id):
        week = self.get_week(request, week_id)
        if week.is_closed:
            return Response({'detail': 'Week is closed.'}, status=400)
        writer = WeekWriteSerializer()
        week = writer.update_week(week, request.data)
        return Response(WeekDetailSerializer(week).data)


class WeekFlowboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, week_id):
        week = get_object_or_404(Week, user=request.user, start_date=week_id)
        return Response(WeekDetailSerializer(week).data)


class WeekCloseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, week_id):
        week = get_object_or_404(Week, user=request.user, start_date=week_id)
        result = close_week(week)
        return Response(
            {
                'week': WeekDetailSerializer(result['week']).data,
                'awarded_badges': result.get('awarded_badges', []),
            }
        )


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(build_dashboard_payload(request.user))


class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        weeks = Week.objects.filter(user=request.user).order_by('-start_date')
        return Response(WeekListSerializer(weeks, many=True).data)


class BadgesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from .models import BadgeProgress, UserBadge

        progress, _ = BadgeProgress.objects.get_or_create(user=request.user)
        badges = UserBadge.objects.filter(user=request.user)
        return Response(
            {
                'progress': {
                    'streak_position': progress.streak_position,
                    'tier': progress.tier,
                    'crowns_earned': progress.crowns_earned,
                },
                'earned': UserBadgeSerializer(badges, many=True).data,
            }
        )


class ScanListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        scans = ScanUpload.objects.filter(user=request.user).order_by('-created_at')[:20]
        return Response(ScanUploadSerializer(scans, many=True).data)

    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({'detail': 'Image required.'}, status=400)
        scan = ScanUpload.objects.create(user=request.user, image=image)
        process_scan.delay(scan.id)
        return Response(ScanUploadSerializer(scan).data, status=201)


class ScanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        scan = get_object_or_404(ScanUpload, pk=pk, user=request.user)
        return Response(ScanUploadSerializer(scan).data)


class ScanConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        scan = get_object_or_404(ScanUpload, pk=pk, user=request.user)
        week = Week.objects.filter(user=request.user, is_current=True).first()
        if not week:
            return Response({'detail': 'No current week.'}, status=400)
        draft = scan.ocr_raw.get('draft', {})
        writer = WeekWriteSerializer()
        writer.update_week(week, draft)
        scan.week = week
        scan.status = ScanUpload.STATUS_COMPLETED
        scan.save()
        return Response(WeekDetailSerializer(week).data)
