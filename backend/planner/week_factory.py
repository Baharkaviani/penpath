from datetime import date, timedelta

from .models import FlameRating, Reflection, Task, Week
from .services import CORE_ROWS, SIDE_ROWS


def ensure_current_week(user):
    """Return the user's current week, creating one with empty task rows if needed."""
    week = Week.objects.filter(user=user, is_current=True).first()
    if week:
        return week

    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    label = f'{start.strftime("%b %d")} – {end.strftime("%b %d, %Y")}'

    Week.objects.filter(user=user, is_current=True).update(is_current=False)

    week = Week.objects.create(
        user=user,
        start_date=start,
        end_date=end,
        label=label,
        is_current=True,
        is_closed=False,
    )
    for i in range(CORE_ROWS):
        Task.objects.create(week=week, kind=Task.KIND_CORE, sort_order=i)
    for i in range(SIDE_ROWS):
        Task.objects.create(week=week, kind=Task.KIND_SIDE, sort_order=i)
    for dim, _ in FlameRating.DIMENSIONS:
        FlameRating.objects.create(week=week, dimension=dim, score=0)
    Reflection.objects.create(week=week, lines=['', '', '', ''])
    return week
