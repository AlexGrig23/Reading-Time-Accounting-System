from datetime import timedelta

import pytest

from auth_api.models import UserReadingStats


@pytest.mark.django_db(transaction=True)
def test_create_user_reading_stats(create_user):
    reading_stats = UserReadingStats.objects.get(user=create_user)

    assert reading_stats.user == create_user
    assert reading_stats.statistic_time_7_days == timedelta(days=0)
    assert reading_stats.statistic_time_30_days == timedelta(days=0)
    assert str(reading_stats) == f"Reading statistics for {create_user.username}"


@pytest.mark.django_db(transaction=True)
def test_delete_user_also_deletes_reading_stats(create_user):
    user_id = create_user.id
    create_user.delete()

    assert not UserReadingStats.objects.filter(user_id=user_id).exists()
