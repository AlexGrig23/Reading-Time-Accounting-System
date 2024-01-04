# Description: Views for library app.
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import Book, ReadingSession
from library.serializers import (
    BookListSerializer,
    BookRetrieveSerializer,
    EndReadingSessionSerializer,
    StartReadingSessionSerializer,
)


class BaseBookView:
    """
    Base class for Book views.
    BaseBookView may contain general configuration or methods that are used
    in several book representation classes.
    """

    queryset = Book.objects.all()


class BookListView(BaseBookView, ListAPIView):
    """
    View for list books.
    Usage example:
    GET api/v1/library/books/
    """

    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]


class BookRetrieveView(BaseBookView, RetrieveAPIView):
    """
    View for retrieve book.
    :param pk: Book id.
    Usage example:
    GET api/v1/library/books/ { "book_id": 1 }
    """

    serializer_class = BookRetrieveSerializer
    permission_classes = [IsAuthenticated]


class StartReadingSessionView(CreateAPIView):
    """
    View for start reading session.
    Method create() is used to create a record of the start of a new book reading session by the user.
    Usage example:
    POST api/v1/library/sessions/ { "book_id": 1 } /start
    """

    queryset = ReadingSession.objects.all()
    serializer_class = StartReadingSessionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create reading session for user.
        This method is used to create a record of the start of a new book reading session by the user.
        Before creating a new session, all previous active reading sessions are automatically closed
        this user to ensure that only one reading session is active at a time.

        :param request: Request object from the user. Includes user data and other metadata.
        :param args: Additional positional arguments (not used in this method).
        :param kwargs: Expected to contain the 'book_id' key, which points to the book ID for the reading session.
        :return: HTTP response with new reading session data if creation was successful, otherwise -
              response with the appropriate error status.
        """
        book = get_object_or_404(Book, pk=kwargs.get("book_id"))
        EndReadingSessionView.end_active_sessions(request.user)

        reading_session = ReadingSession.objects.create(
            user=request.user, book=book, status=True
        )
        serializer = self.get_serializer(reading_session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EndReadingSessionView(APIView):
    """
    View for end reading session.
    Method update() is used to close the active reading session for the user.
    Usage example:
    PATCH api/v1/library/sessions/ { "book_id": 1 } /end
    """

    queryset = ReadingSession.objects.all()
    serializer_class = EndReadingSessionSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def end_active_sessions(user, book_id=None):
        """
        Close all active reading sessions for the user.
        :param user: User object whose reading sessions should be closed.
        :param book_id: Optional book identifier. If provided, the method will close
                    only the reading sessions of that particular book. If not provided,
                    All active reading sessions of the user will be closed.

        :return: A Boolean value indicating whether the user has had active reading sessions.
                Returns True if there were active sessions and they were closed. Returns False
                if there were no active sessions.

            Process:
         1. A query is generated to select all active reading sessions of the user.
         2. If a book_id is provided, the request is further filtered by the book ID.
         3. Checks for active sessions.
         4. If there are active sessions, they are updated - the end time is set and the status is 'inactive'.
        """
        active_sessions_query = ReadingSession.objects.filter(user=user, status=True)

        if book_id is not None:
            active_sessions_query = active_sessions_query.filter(book_id=book_id)

        active_sessions = active_sessions_query.exists()

        if active_sessions:
            active_sessions_query.update(end_time=timezone.now(), status=False)

        return active_sessions

    def patch(self, request, *args, **kwargs):
        """
        Close the active reading session for the user.
        :param request: Request object from the user. Includes user data and other metadata.
        :param args: Additional positional arguments (not used in this method).
        :param kwargs: Expected to contain the 'book_id' key, which points to the book ID for the reading session.
        :return: HTTP response with a message about successful closing of the reading session or an error message,
              if no active reading session is found.
        """
        book = get_object_or_404(Book, pk=kwargs.get("book_id"))

        if not self.end_active_sessions(request.user, book.pk):
            return Response(
                {"message": "No active reading session found for this book."},
                status=status.HTTP_404_NOT_FOUND,
            )

        EndReadingSessionView.end_active_sessions(request.user)
        return Response(
            {"message": "Reading session closed."}, status=status.HTTP_200_OK
        )
