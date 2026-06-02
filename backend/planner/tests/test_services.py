from django.contrib.auth.models import User
from django.test import TestCase

from planner.models import BadgeProgress, Task, Week
from planner.services import close_week, is_win, weekly_score


class ScoreTests(TestCase):
    def test_weekly_score_formula(self):
        self.assertEqual(weekly_score(78, 92), 82)
        self.assertEqual(weekly_score(80, 70), 77)

    def test_is_win_threshold(self):
        self.assertTrue(is_win(80))
        self.assertFalse(is_win(79))


class BadgeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', password='test')
        BadgeProgress.objects.create(user=self.user, streak_position=0, tier=1)

    def _make_week(self, core, side, win=None):
        score = weekly_score(core, side)
        week = Week.objects.create(
            user=self.user,
            start_date='2026-01-01',
            end_date='2026-01-07',
            label='Test week',
            core_rate=core,
            side_rate=side,
            weekly_score=score,
            is_win=win if win is not None else is_win(score),
            is_current=True,
        )
        for i in range(7):
            Task.objects.create(
                week=week, kind=Task.KIND_CORE, sort_order=i, tracker_filled=12
            )
        for i in range(5):
            Task.objects.create(
                week=week, kind=Task.KIND_SIDE, sort_order=i, tracker_filled=12
            )
        return week

    def test_win_advances_streak(self):
        week = self._make_week(90, 90)
        close_week(week)
        progress = BadgeProgress.objects.get(user=self.user)
        self.assertEqual(progress.streak_position, 1)

    def test_loss_resets_streak(self):
        week = self._make_week(50, 50)
        close_week(week)
        progress = BadgeProgress.objects.get(user=self.user)
        self.assertEqual(progress.streak_position, 0)
        self.assertTrue(progress.last_week_was_loss)
