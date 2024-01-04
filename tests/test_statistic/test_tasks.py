import pytest

from auth_api.models import UserReadingStats
from statistic.tasks import UserReadingStatsUpdater, update_user_reading_stats_7_days, update_user_reading_stats_30_days


@pytest.mark.django_db
def test_update_user_reading_stats_7_days(create_reading_sessions):
    users = create_reading_sessions(days_before_now=3, duration_hours=1)
    UserReadingStatsUpdater.update_user_reading_stats(7)

    for user in users:
        stats = UserReadingStats.objects.get(user=user)
        assert stats.statistic_time_7_days is not None


@pytest.mark.django_db
def test_update_user_reading_stats_30_days(create_reading_sessions):
    users = create_reading_sessions(days_before_now=10, duration_hours=4)
    UserReadingStatsUpdater.update_user_reading_stats(30)

    for user in users:
        stats = UserReadingStats.objects.get(user=user)
        assert stats.statistic_time_30_days is not None


@pytest.mark.django_db
def test_celery_task_update_user_reading_stats_7_days(mocker):
    mock_update = mocker.patch(
        "statistic.tasks.UserReadingStatsUpdater.update_user_reading_stats"
    )
    update_user_reading_stats_7_days()

    mock_update.assert_called_once_with(7)


@pytest.mark.django_db
def test_celery_task_update_user_reading_stats_30_days(mocker):
    mock_update = mocker.patch(
        "statistic.tasks.UserReadingStatsUpdater.update_user_reading_stats"
    )
    update_user_reading_stats_30_days()

    mock_update.assert_called_once_with(30)
