from django.urls import path

from . import views

urlpatterns = [
    path('me/', views.MeView.as_view()),
    path('auth/csrf/', views.CsrfView.as_view()),
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/login/', views.LoginView.as_view()),
    path('auth/logout/', views.LogoutView.as_view()),
    path('weeks/', views.WeekListCreateView.as_view()),
    path('weeks/current/', views.CurrentWeekView.as_view()),
    path('weeks/<str:week_id>/', views.WeekDetailView.as_view()),
    path('weeks/<str:week_id>/flowboard/', views.WeekFlowboardView.as_view()),
    path('weeks/<str:week_id>/close/', views.WeekCloseView.as_view()),
    path('dashboard/', views.DashboardView.as_view()),
    path('history/', views.HistoryView.as_view()),
    path('badges/', views.BadgesView.as_view()),
    path('scans/', views.ScanListCreateView.as_view()),
    path('scans/<int:pk>/', views.ScanDetailView.as_view()),
    path('scans/<int:pk>/confirm/', views.ScanConfirmView.as_view()),
]
