# Description: URL patterns for the library app
from django.urls import path

from library.views import BookListView, BookRetrieveView, EndReadingSessionView, StartReadingSessionView

urlpatterns = [
    path("books/", BookListView.as_view(), name="books"),
    path("books/<int:pk>", BookRetrieveView.as_view(), name="book-detail"),
    path(
        "sessions/<int:book_id>/start",
        StartReadingSessionView.as_view(),
        name="start-reading-session",
    ),
    path(
        "sessions/<int:book_id>/end",
        EndReadingSessionView.as_view(),
        name="end-reading-session",
    ),
]
