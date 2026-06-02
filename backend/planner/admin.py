from django.contrib import admin

from .models import (
    BadgeProgress,
    FlameRating,
    Reflection,
    ScanUpload,
    Task,
    UserBadge,
    Week,
)


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class FlameInline(admin.TabularInline):
    model = FlameRating
    extra = 0


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ['label', 'user', 'weekly_score', 'is_win', 'is_current', 'is_closed']
    list_filter = ['is_current', 'is_closed', 'is_win']
    inlines = [TaskInline, FlameInline]


@admin.register(ScanUpload)
class ScanUploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at']


@admin.register(BadgeProgress)
class BadgeProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'streak_position', 'tier', 'crowns_earned']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge_type', 'tier', 'earned_at']
