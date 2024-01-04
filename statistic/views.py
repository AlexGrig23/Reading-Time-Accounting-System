from datetime import timedelta

from django.db.models import DurationField, ExpressionWrapper, F, Q, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library.models import Book

from .serializers import BookReadingTimeSerializer, UserReadingStatsSerializer


class BaseReadingTimeView:
    """
    Base class for Book views.
    BaseBookView may contain general configuration or methods that are used
    in several book representation classes.
    Methods:
        :static aggregate_reading_time()
    """

    @staticmethod
    def aggregate_reading_time(queryset, user=None):
        """
        Method for aggregate reading time.
        This method annotates each book in the queryset with the total reading time based on related reading sessions.
        It includes an option to filter the reading sessions by a specific user.

        :param queryset:  A queryset of Book instances to be annotated.
        :param user: An optional User instance for which to filter the reading sessions.
                If provided, only reading sessions for this user are considered in the aggregation.
        :return: The annotated queryset with each book having an additional 'total_reading_time'
                attribute representing the sum of the duration of reading sessions associated with the book.
                Books with no reading time (zero duration) are excluded.
        """
        filter_kwargs = {"readingsession__end_time__isnull": False}
        if user:
            filter_kwargs["readingsession__user"] = user

        aggregated_queryset = queryset.annotate(
            total_reading_time=Sum(
                Coalesce(
                    ExpressionWrapper(
                        F("readingsession__end_time") - F("readingsession__start_time"),
                        output_field=DurationField(),
                    ),
                    Value(timedelta()),
                    output_field=DurationField(),
                ),
                filter=Q(**filter_kwargs),
            )
        ).distinct()

        return aggregated_queryset.filter(total_reading_time__gt=timedelta(0))


class BookReadingTimeListView(BaseReadingTimeView, ListAPIView):
    """
    View for list books with total reading time.
    Usage example:
    GET api/v1/statistic/books/
    """

    serializer_class = BookReadingTimeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.aggregate_reading_time(Book.objects.all())


class BookReadingTimeRetrieveView(BaseReadingTimeView, RetrieveAPIView):
    """
    View for retrieve book with total reading time.
    :param pk: Book id.
    Usage example:
    GET api/v1/statistic/books/ { "book_id": 1 }
    """

    serializer_class = BookReadingTimeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs.get("pk")
        return self.aggregate_reading_time(Book.objects.filter(id=book_id))


class UserBookReadingTimeListView(BaseReadingTimeView, ListAPIView):
    """
    View for list books with total reading time for user.
    Usage example:
    GET api/v1/statistic/user/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        books_queryset = self.aggregate_reading_time(Book.objects.all(), user=user)

        books_serializer = BookReadingTimeSerializer(books_queryset, many=True)
        all_statistics_serializer = UserReadingStatsSerializer(user.reading_stats)

        response_data = {
            "username": user.username,
            "statistics": all_statistics_serializer.data,
            "books": books_serializer.data,
        }
        return Response(response_data)
