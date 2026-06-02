"""Load demo weeks with sample flowboard data."""

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from planner.models import BadgeProgress, FlameRating, Reflection, Task, UserBadge, Week
from planner.services import CORE_ROWS, SIDE_ROWS, update_week_scores

DEMO_WEEKS = [
    {
        'id': '2026-05-26',
        'label': 'May 26 – Jun 1, 2026',
        'focus': 'Ship flowboard OCR prototype',
        'prize': 'Coffee + long walk Sunday',
        'core': 78,
        'side': 92,
        'score': 84,
        'win': True,
        'flame': 4.3,
        'isCurrent': True,
        'coreTasks': [
            {'goal': 'OCR upload endpoint', 'why': 'Unlock scan flow', 'time': '8h', 'notes': 'API stub done', 'trackerFilled': 11},
            {'goal': 'Vue flowboard view', 'why': 'Match paper layout', 'time': '6h', 'notes': '', 'trackerFilled': 10},
            {'goal': 'Badge rule tests', 'why': 'Trust the streak', 'time': '3h', 'notes': '', 'trackerFilled': 8},
            {'goal': 'Docker docs', 'why': 'Easy onboarding', 'time': '2h', 'notes': '', 'trackerFilled': 7},
        ],
        'sideTasks': [
            {'goal': 'Gym × 3', 'why': 'Energy for FLAME', 'time': '4h', 'notes': '2/3 done', 'trackerFilled': 12},
            {'goal': 'Inbox zero Friday', 'why': 'Clear head', 'time': '1h', 'notes': '', 'trackerFilled': 9},
        ],
        'flameRatings': {'focus': 4, 'leverage': 5, 'alignment': 4, 'momentum': 4, 'energy': 3, 'fulfillment': 5},
        'reflection': ['Strong build week; OCR is the main risk.', 'Keep morning deep-work blocks.', 'Add reviewer step before marking week complete.', ''],
    },
    {
        'id': '2026-05-19',
        'label': 'May 19 – May 25, 2026',
        'focus': 'Database models & admin',
        'prize': 'Nice dinner out',
        'core': 85,
        'side': 70,
        'score': 80,
        'win': True,
        'flame': 4.1,
        'isCurrent': False,
        'coreTasks': [
            {'goal': 'Week & Task models', 'why': 'Foundation', 'time': '10h', 'notes': 'Shipped', 'trackerFilled': 13},
            {'goal': 'Django admin', 'why': 'Manual QA', 'time': '4h', 'notes': '', 'trackerFilled': 12},
            {'goal': 'Migrations', 'why': 'Deployable', 'time': '2h', 'notes': '', 'trackerFilled': 11},
        ],
        'sideTasks': [
            {'goal': 'Read 1 chapter', 'why': 'Learning', 'time': '2h', 'notes': '', 'trackerFilled': 8},
            {'goal': 'Meal prep', 'why': 'Health', 'time': '2h', 'notes': '', 'trackerFilled': 7},
        ],
        'flameRatings': {'focus': 4, 'leverage': 4, 'alignment': 4, 'momentum': 4, 'energy': 4, 'fulfillment': 4},
        'reflection': ['Models week went smoothly.', 'Document schema for frontend team.', 'Schedule user test for scan flow.', ''],
    },
    {
        'id': '2026-05-12',
        'label': 'May 12 – May 18, 2026',
        'focus': 'Recover momentum after travel',
        'prize': 'Movie night',
        'core': 62,
        'side': 55,
        'score': 60,
        'win': False,
        'flame': 3.2,
        'isCurrent': False,
        'coreTasks': [
            {'goal': 'Catch up on email', 'why': 'Clear deck', 'time': '3h', 'notes': 'Partial', 'trackerFilled': 6},
            {'goal': 'Restart gym', 'why': 'Energy', 'time': '3h', 'notes': '1 session', 'trackerFilled': 4},
        ],
        'sideTasks': [
            {'goal': 'Unpack & organize', 'why': 'Home baseline', 'time': '2h', 'notes': '', 'trackerFilled': 5},
        ],
        'flameRatings': {'focus': 3, 'leverage': 3, 'alignment': 3, 'momentum': 2, 'energy': 3, 'fulfillment': 4},
        'reflection': ['Travel knocked me off rhythm — expected.', 'Phoenix week: win the next one.', 'Block calendar before trips.', ''],
    },
]


class Command(BaseCommand):
    help = 'Create demo user and seed weeks (username: demo, password: demo)'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username='demo', defaults={'email': 'demo@penpath.local'})
        if created:
            user.set_password('demo')
            user.save()
            self.stdout.write('Created user demo / demo')
        else:
            user.set_password('demo')
            user.save()
            Week.objects.filter(user=user).delete()
            UserBadge.objects.filter(user=user).delete()

        BadgeProgress.objects.update_or_create(
            user=user,
            defaults={'streak_position': 3, 'tier': 1, 'crowns_earned': 0, 'last_week_was_loss': False},
        )

        for data in DEMO_WEEKS:
            start = date.fromisoformat(data['id'])
            end = start + timedelta(days=6)
            week, _ = Week.objects.update_or_create(
                user=user,
                start_date=start,
                defaults={
                    'end_date': end,
                    'label': data['label'],
                    'focus': data.get('focus', ''),
                    'prize': data.get('prize', ''),
                    'core_rate': data['core'],
                    'side_rate': data['side'],
                    'weekly_score': data['score'],
                    'is_win': data['win'],
                    'flame_average': data['flame'],
                    'is_current': data.get('isCurrent', False),
                    'is_closed': not data.get('isCurrent', False),
                },
            )
            week.tasks.all().delete()
            for i in range(CORE_ROWS):
                row = (data.get('coreTasks') or [{}])[i] if i < len(data.get('coreTasks') or []) else {}
                Task.objects.create(
                    week=week,
                    kind=Task.KIND_CORE,
                    sort_order=i,
                    goal=row.get('goal', ''),
                    why=row.get('why', ''),
                    est_time=row.get('time', ''),
                    notes=row.get('notes', ''),
                    tracker_filled=row.get('trackerFilled', 0),
                )
            for i in range(SIDE_ROWS):
                row = (data.get('sideTasks') or [{}])[i] if i < len(data.get('sideTasks') or []) else {}
                Task.objects.create(
                    week=week,
                    kind=Task.KIND_SIDE,
                    sort_order=i,
                    goal=row.get('goal', ''),
                    why=row.get('why', ''),
                    est_time=row.get('time', ''),
                    notes=row.get('notes', ''),
                    tracker_filled=row.get('trackerFilled', 0),
                )
            for dim, score in (data.get('flameRatings') or {}).items():
                FlameRating.objects.update_or_create(week=week, dimension=dim, defaults={'score': score})
            Reflection.objects.update_or_create(week=week, defaults={'lines': data.get('reflection', [''] * 4)})
            if data.get('isCurrent'):
                update_week_scores(week)

        self.stdout.write(self.style.SUCCESS('Demo data seeded. Login: demo / demo'))
