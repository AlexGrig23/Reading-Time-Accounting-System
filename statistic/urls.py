# Description: Urls for statistic app
from django.urls import path

from statistic.views import BookReadingTimeListView, BookReadingTimeRetrieveView, UserBookReadingTimeListView

urlpatterns = [
    path("users/", UserBookReadingTimeListView.as_view(), name="users-statistic"),
    path("books/", BookReadingTimeListView.as_view(), name="books-statistic"),
    path(
        "books/<int:pk>",
        BookReadingTimeRetrieveView.as_view(),
        name="books-retrieve-statistic",
    ),
]
