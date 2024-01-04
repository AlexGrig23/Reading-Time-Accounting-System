# Description: Serializers for statistic app
from rest_framework import serializers

from auth_api.models import UserReadingStats
from library.models import Book


class BookReadingTimeSerializer(serializers.ModelSerializer):
    total_reading_time = serializers.DurationField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "year", "author", "total_reading_time"]


class UserReadingStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReadingStats
        fields = ["statistic_time_7_days", "statistic_time_30_days"]
