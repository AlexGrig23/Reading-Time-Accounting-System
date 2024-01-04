from datetime import timedelta

import pytest

from statistic.serializers import BookReadingTimeSerializer, UserReadingStatsSerializer


@pytest.mark.django_db
def test_book_reading_time_serializer_validation(create_book):
    book_data = {
        "title": create_book.title,
        "author": create_book.author,
        "year": create_book.year,
    }

    serializer = BookReadingTimeSerializer(data=book_data)
    assert serializer.is_valid()
    book = serializer.save()

    assert book.title == book_data["title"]
    assert book.author == book_data["author"]
    assert book.year == book_data["year"]


def test_book_reading_time_serializer_read_only_field(create_book):
    book_data = {
        "title": create_book.title,
        "author": create_book.author,
        "year": create_book.year,
        "total_reading_time": timedelta(hours=2),
    }

    serializer = BookReadingTimeSerializer(data=book_data)
    assert serializer.is_valid()
    book = serializer.save()

    assert not hasattr(book, "total_reading_time")

    book.total_reading_time = timedelta(hours=2)
    serializer = BookReadingTimeSerializer(book)
    assert "total_reading_time" in serializer.data
    assert serializer.data["total_reading_time"] is not None


@pytest.mark.django_db
def test_user_reading_stats_serializer(user_reading_stats):
    serializer = UserReadingStatsSerializer(instance=user_reading_stats)
    assert serializer.data["statistic_time_7_days"] == "7 00:00:00"
    assert serializer.data["statistic_time_30_days"] == "30 00:00:00"


@pytest.mark.django_db
def test_user_reading_stats_deserialization(user_reading_stats):
    user_data = {
        "statistic_time_7_days": "7:00:00",
        "statistic_time_30_days": "30:00:00",
    }

    serializer = UserReadingStatsSerializer(instance=user_reading_stats, data=user_data)
    assert serializer.is_valid()
    user_stats = serializer.save()

    assert user_stats.statistic_time_7_days == timedelta(hours=7)
    assert user_stats.statistic_time_30_days == timedelta(hours=30)
