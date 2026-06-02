from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    BadgeProgress,
    FlameRating,
    Reflection,
    ScanUpload,
    Task,
    UserBadge,
    Week,
)
from .services import update_week_scores

User = get_user_model()

FLAME_LETTERS = {
    'focus': ('F', 'Focus'),
    'leverage': ('L', 'Leverage'),
    'alignment': ('A', 'Alignment'),
    'momentum': ('M', 'Momentum'),
    'energy': ('E', 'Energy'),
    'fulfillment': ('+', 'Fulfillment'),
}


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'kind', 'sort_order', 'goal', 'why', 'est_time', 'notes', 'tracker_filled']


class FlameRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlameRating
        fields = ['dimension', 'score']


class ReflectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reflection
        fields = ['lines']


class WeekListSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    weekShort = serializers.SerializerMethodField()
    core = serializers.IntegerField(source='core_rate')
    side = serializers.IntegerField(source='side_rate')
    score = serializers.IntegerField(source='weekly_score')
    win = serializers.BooleanField(source='is_win')
    flame = serializers.DecimalField(source='flame_average', max_digits=3, decimal_places=1)

    class Meta:
        model = Week
        fields = [
            'id',
            'label',
            'weekShort',
            'core',
            'side',
            'score',
            'win',
            'flame',
            'is_current',
            'start_date',
        ]

    def get_id(self, obj):
        return obj.week_id

    def get_weekShort(self, obj):
        return obj.start_date.strftime('%b %d')


class WeekDetailSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    weekShort = serializers.SerializerMethodField()
    core = serializers.IntegerField(source='core_rate', read_only=True)
    side = serializers.IntegerField(source='side_rate', read_only=True)
    score = serializers.IntegerField(source='weekly_score', read_only=True)
    win = serializers.BooleanField(source='is_win', read_only=True)
    flame = serializers.DecimalField(source='flame_average', max_digits=3, decimal_places=1, read_only=True)
    isCurrent = serializers.BooleanField(source='is_current')
    coreTasks = serializers.SerializerMethodField()
    sideTasks = serializers.SerializerMethodField()
    flameRatings = serializers.SerializerMethodField()
    reflection = serializers.SerializerMethodField()

    class Meta:
        model = Week
        fields = [
            'id',
            'label',
            'weekShort',
            'focus',
            'prize',
            'core',
            'side',
            'score',
            'win',
            'flame',
            'isCurrent',
            'is_closed',
            'start_date',
            'end_date',
            'coreTasks',
            'sideTasks',
            'flameRatings',
            'reflection',
        ]

    def get_id(self, obj):
        return obj.week_id

    def get_weekShort(self, obj):
        return obj.start_date.strftime('%b %d')

    def _task_dict(self, task):
        return {
            'goal': task.goal,
            'why': task.why,
            'time': task.est_time,
            'notes': task.notes,
            'trackerFilled': task.tracker_filled,
        }

    def get_coreTasks(self, obj):
        tasks = obj.tasks.filter(kind=Task.KIND_CORE).order_by('sort_order')
        rows = [self._task_dict(t) for t in tasks]
        while len(rows) < 7:
            rows.append({'goal': '', 'why': '', 'time': '', 'notes': '', 'trackerFilled': 0})
        return rows[:7]

    def get_sideTasks(self, obj):
        tasks = obj.tasks.filter(kind=Task.KIND_SIDE).order_by('sort_order')
        rows = [self._task_dict(t) for t in tasks]
        while len(rows) < 5:
            rows.append({'goal': '', 'why': '', 'time': '', 'notes': '', 'trackerFilled': 0})
        return rows[:5]

    def get_flameRatings(self, obj):
        ratings = {r.dimension: r.score for r in obj.flame_ratings.all()}
        for dim, _ in FlameRating.DIMENSIONS:
            ratings.setdefault(dim, 0)
        return ratings

    def get_reflection(self, obj):
        if hasattr(obj, 'reflection'):
            lines = obj.reflection.lines or []
        else:
            lines = []
        while len(lines) < 4:
            lines.append('')
        return lines[:4]


class WeekWriteSerializer(serializers.Serializer):
    focus = serializers.CharField(required=False, allow_blank=True)
    prize = serializers.CharField(required=False, allow_blank=True)
    coreTasks = serializers.ListField(child=serializers.DictField(), required=False)
    sideTasks = serializers.ListField(child=serializers.DictField(), required=False)
    flameRatings = serializers.DictField(child=serializers.IntegerField(), required=False)
    reflection = serializers.ListField(child=serializers.CharField(), required=False)

    def update_week(self, week, data):
        if 'focus' in data:
            week.focus = data['focus']
        if 'prize' in data:
            week.prize = data['prize']
        week.save()

        if 'coreTasks' in data:
            self._save_tasks(week, Task.KIND_CORE, data['coreTasks'], 7)
        if 'sideTasks' in data:
            self._save_tasks(week, Task.KIND_SIDE, data['sideTasks'], 5)
        if 'flameRatings' in data:
            for dim, score in data['flameRatings'].items():
                if dim in dict(FlameRating.DIMENSIONS):
                    FlameRating.objects.update_or_create(
                        week=week, dimension=dim, defaults={'score': score or 0}
                    )
        if 'reflection' in data:
            Reflection.objects.update_or_create(week=week, defaults={'lines': data['reflection']})
        update_week_scores(week)
        return week

    def _save_tasks(self, week, kind, rows, count):
        for i in range(count):
            row = rows[i] if i < len(rows) else {}
            Task.objects.update_or_create(
                week=week,
                kind=kind,
                sort_order=i,
                defaults={
                    'goal': row.get('goal', ''),
                    'why': row.get('why', ''),
                    'est_time': row.get('time', row.get('est_time', '')),
                    'notes': row.get('notes', ''),
                    'tracker_filled': min(14, max(0, int(row.get('trackerFilled', 0)))),
                },
            )


class ScanUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanUpload
        fields = ['id', 'status', 'ocr_raw', 'week', 'created_at']
        read_only_fields = ['status', 'ocr_raw', 'week', 'created_at']


class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = ['badge_type', 'tier', 'earned_at']


class BadgeProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeProgress
        fields = ['streak_position', 'tier', 'crowns_earned', 'last_week_was_loss']


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


def build_dashboard_payload(user):
    current = Week.objects.filter(user=user, is_current=True).first()
    if not current:
        current = Week.objects.filter(user=user).order_by('-start_date').first()

    weeks = Week.objects.filter(user=user, is_closed=True).order_by('start_date')
    chart_bars = [
        {
            'label': w.start_date.strftime('%b %d'),
            'height': w.weekly_score,
            'win': w.is_win,
            'weekId': w.week_id,
        }
        for w in weeks
    ]

    progress, _ = BadgeProgress.objects.get_or_create(user=user)
    badges = UserBadge.objects.filter(user=user)

    flame_list = []
    if current:
        for dim, (letter, name) in FLAME_LETTERS.items():
            rating = current.flame_ratings.filter(dimension=dim).first()
            score = rating.score if rating else 0
            flame_list.append({'letter': letter, 'name': name, 'score': score})

    closed_count = weeks.count()
    wins = weeks.filter(is_win=True).count()
    win_rate = round((wins / closed_count) * 100) if closed_count else 0

    return {
        'stats': {
            'weeklyScore': current.weekly_score if current else 0,
            'coreRate': current.core_rate if current else 0,
            'sideRate': current.side_rate if current else 0,
            'winThreshold': 80,
            'streakWeek': progress.streak_position,
            'tier': progress.tier,
            'crownsEarned': progress.crowns_earned,
            'phoenixCount': badges.filter(badge_type='phoenix').count(),
            'avgFlame': float(current.flame_average) if current else 0,
            'weeksTracked': Week.objects.filter(user=user).count(),
            'winRate': win_rate,
        },
        'flame': flame_list,
        'chartBars': chart_bars,
        'currentWeek': WeekDetailSerializer(current).data if current else None,
        'badgeProgress': BadgeProgressSerializer(progress).data,
        'earnedBadges': UserBadgeSerializer(badges, many=True).data,
    }
