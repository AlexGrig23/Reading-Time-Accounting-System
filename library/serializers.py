# Description: Serializers for library app.
from rest_framework import serializers

from library.models import Book, ReadingSession


class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing books, with less detail.
    """

    class Meta:
        model = Book
        fields = ["id", "title", "author", "year", "short_description"]


class BookRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed book view, including last read date.
    Method get_last_read_date() is used to get the date of the last reading session.
    """

    last_read_date = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "year",
            "short_description",
            "full_description",
            "last_read_date",
        ]

    def get_last_read_date(self, obj):
        """
        Get the date of the last reading session.
        :param obj:
        :return:
        """
        last_reading_session = obj.readingsession_set.last()
        return last_reading_session.end_time if last_reading_session else None


class StartReadingSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for ReadingSession model.
    """

    class Meta:
        model = ReadingSession
        fields = ["user", "book", "start_time"]


class EndReadingSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for ReadingSession model.
    """

    class Meta:
        model = ReadingSession
        fields = ["user", "book", "end_time"]
