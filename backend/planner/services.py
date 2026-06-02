"""Score computation and badge progression (see README)."""

from decimal import Decimal

from django.db import transaction

from .models import BadgeProgress, Task, UserBadge, Week

WIN_THRESHOLD = 80
TRACKER_COUNT = 14
CORE_ROWS = 7
SIDE_ROWS = 5
STREAK_BADGE_MAP = {1: 'seed', 2: 'flame', 3: 'garden', 4: 'gem'}


def weekly_score(core_rate: int, side_rate: int) -> int:
    return round(0.7 * core_rate + 0.3 * side_rate)


def is_win(score: int, threshold: int = WIN_THRESHOLD) -> bool:
    return score >= threshold


def compute_rates_from_tasks(week: Week) -> tuple[int, int]:
    core_tasks = week.tasks.filter(kind=Task.KIND_CORE)
    side_tasks = week.tasks.filter(kind=Task.KIND_SIDE)

    core_filled = sum(t.tracker_filled for t in core_tasks)
    core_total = core_tasks.count() * TRACKER_COUNT
    side_filled = sum(t.tracker_filled for t in side_tasks)
    side_total = side_tasks.count() * TRACKER_COUNT

    core_rate = round((core_filled / core_total) * 100) if core_total else 0
    side_rate = round((side_filled / side_total) * 100) if side_total else 0
    return core_rate, side_rate


def compute_flame_average(week: Week) -> Decimal:
    ratings = list(week.flame_ratings.values_list('score', flat=True))
    if not ratings:
        return Decimal('0')
    return Decimal(str(round(sum(ratings) / len(ratings), 1)))


def update_week_scores(week: Week) -> Week:
    core_rate, side_rate = compute_rates_from_tasks(week)
    score = weekly_score(core_rate, side_rate)
    week.core_rate = core_rate
    week.side_rate = side_rate
    week.weekly_score = score
    week.is_win = is_win(score)
    week.flame_average = compute_flame_average(week)
    week.save(
        update_fields=[
            'core_rate',
            'side_rate',
            'weekly_score',
            'is_win',
            'flame_average',
            'updated_at',
        ]
    )
    return week


def _award_badge(user, badge_type: str, tier: int):
    if UserBadge.objects.filter(user=user, badge_type=badge_type, tier=tier).exists():
        return
    UserBadge.objects.create(user=user, badge_type=badge_type, tier=tier)


@transaction.atomic
def close_week(week: Week) -> dict:
    """Finalize week: scores, badge progression, return summary."""
    if week.is_closed:
        return {'already_closed': True}

    week = update_week_scores(week)
    week.is_closed = True
    week.is_current = False
    week.save(update_fields=['is_closed', 'is_current', 'updated_at'])

    progress, _ = BadgeProgress.objects.get_or_create(user=week.user)
    awarded = []

    if week.is_win:
        if progress.last_week_was_loss:
            _award_badge(week.user, 'phoenix', progress.tier)
            awarded.append('phoenix')
            progress.streak_position = 1
            _award_badge(week.user, STREAK_BADGE_MAP[1], progress.tier)
            awarded.append(STREAK_BADGE_MAP[1])
        else:
            new_pos = min(progress.streak_position + 1, 4)
            progress.streak_position = new_pos
            badge = STREAK_BADGE_MAP[new_pos]
            _award_badge(week.user, badge, progress.tier)
            awarded.append(badge)
            if new_pos == 4:
                _award_badge(week.user, 'crown', progress.tier)
                awarded.append('crown')
                progress.crowns_earned += 1
                progress.tier += 1
                progress.streak_position = 0
        progress.last_week_was_loss = False
    else:
        progress.streak_position = 0
        progress.last_week_was_loss = True

    progress.save()
    return {
        'week': week,
        'awarded_badges': awarded,
        'streak_position': progress.streak_position,
        'tier': progress.tier,
    }

