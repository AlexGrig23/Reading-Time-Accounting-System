from datetime import timedelta

import pytest

from statistic.models import ReadingStatistics


@pytest.mark.django_db
def test_reading_statistics_model(create_book, create_user):
    user = create_user
    book = create_book
    reading_stat = ReadingStatistics.objects.create(
        user=user, book=book, total_reading_time=timedelta(hours=1)
    )

    assert reading_stat.user == user
    assert reading_stat.book == book
    assert reading_stat.total_reading_time == timedelta(hours=1)

    new_reading_stat = ReadingStatistics.objects.create(user=user, book=book)
    assert new_reading_stat.total_reading_time == timedelta()
