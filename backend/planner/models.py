from django.conf import settings
from django.db import models


class Week(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weeks'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    label = models.CharField(max_length=120)
    focus = models.CharField(max_length=500, blank=True)
    prize = models.CharField(max_length=500, blank=True)
    core_rate = models.PositiveSmallIntegerField(default=0)
    side_rate = models.PositiveSmallIntegerField(default=0)
    weekly_score = models.PositiveSmallIntegerField(default=0)
    is_win = models.BooleanField(default=False)
    flame_average = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    is_current = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'start_date'],
                name='unique_user_week_start',
            ),
        ]

    def __str__(self):
        return f'{self.label} ({self.user})'

    @property
    def week_id(self):
        return self.start_date.isoformat()


class Task(models.Model):
    KIND_CORE = 'core'
    KIND_SIDE = 'side'
    KIND_CHOICES = [(KIND_CORE, 'Core'), (KIND_SIDE, 'Side')]

    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='tasks')
    kind = models.CharField(max_length=8, choices=KIND_CHOICES)
    sort_order = models.PositiveSmallIntegerField()
    goal = models.CharField(max_length=500, blank=True)
    why = models.CharField(max_length=500, blank=True)
    est_time = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)
    tracker_filled = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['kind', 'sort_order']
        unique_together = [['week', 'kind', 'sort_order']]


class FlameRating(models.Model):
    DIMENSIONS = [
        ('focus', 'Focus'),
        ('leverage', 'Leverage'),
        ('alignment', 'Alignment'),
        ('momentum', 'Momentum'),
        ('energy', 'Energy'),
        ('fulfillment', 'Fulfillment'),
    ]

    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='flame_ratings')
    dimension = models.CharField(max_length=16, choices=DIMENSIONS)
    score = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = [['week', 'dimension']]


class Reflection(models.Model):
    week = models.OneToOneField(Week, on_delete=models.CASCADE, related_name='reflection')
    lines = models.JSONField(default=list)

    def __str__(self):
        return f'Reflection for {self.week}'


class ScanUpload(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_REVIEW = 'review'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_REVIEW, 'Review'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scans'
    )
    week = models.ForeignKey(
        Week, on_delete=models.SET_NULL, null=True, blank=True, related_name='scans'
    )
    image = models.ImageField(upload_to='scans/%Y/%m/')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    ocr_raw = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BadgeProgress(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badge_progress'
    )
    streak_position = models.PositiveSmallIntegerField(default=0)
    tier = models.PositiveSmallIntegerField(default=1)
    crowns_earned = models.PositiveSmallIntegerField(default=0)
    last_week_was_loss = models.BooleanField(default=False)

    def __str__(self):
        return f'BadgeProgress({self.user}, streak={self.streak_position}, tier={self.tier})'


class UserBadge(models.Model):
    BADGE_TYPES = [
        ('seed', 'Seed of Beginning'),
        ('flame', 'Flame of Focus'),
        ('garden', 'Garden of Growth'),
        ('gem', 'Gem of Balance'),
        ('crown', 'Crown of Consistency'),
        ('phoenix', 'Phoenix of Return'),
    ]
    STREAK_BADGES = ['seed', 'flame', 'garden', 'gem']

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges'
    )
    badge_type = models.CharField(max_length=16, choices=BADGE_TYPES)
    tier = models.PositiveSmallIntegerField(default=1)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['earned_at']
