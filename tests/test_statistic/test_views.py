from datetime import timedelta

import pytest

from library.models import Book
from statistic.views import BaseReadingTimeView


@pytest.mark.django_db
def test_aggregate_reading_time(create_user, create_book, reading_session):
    queryset = Book.objects.all()

    aggregated_queryset = BaseReadingTimeView.aggregate_reading_time(queryset)
    for book in aggregated_queryset:
        if book == create_book:
            assert book.total_reading_time == timedelta(hours=1)
        else:
            assert book.total_reading_time == timedelta(0)

    aggregated_queryset = BaseReadingTimeView.aggregate_reading_time(
        queryset, user=create_user
    )
    for book in aggregated_queryset:
        if book == create_book:
            assert book.total_reading_time == timedelta(hours=1)
        else:
            assert book.total_reading_time == timedelta(0)
