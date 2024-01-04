import pytest
from django.urls import reverse
from rest_framework import status

from library.models import ReadingSession


@pytest.mark.django_db
def test_book_list_access_for_authenticated_user(auth_client):
    url = reverse("books")
    response = auth_client.get(url)
    data = response.data

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(data, list)

    for book in data:
        assert "title" in book
        assert "author" in book
        assert "year" in book
        assert "short_description" in book


@pytest.mark.django_db
def test_book_list_access_for_unauthenticated_user(client):
    url = reverse("books")
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_book_retrieve_with_reading_session_by_authenticated_user(
    auth_client, create_book, end_reading_session
):
    book = create_book
    reading_session = end_reading_session
    url = reverse("book-detail", args=[book.id])
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data["id"] == book.id
    assert response.data["title"] == book.title
    assert response.data["author"] == book.author
    assert response.data["year"] == book.year
    assert response.data["short_description"] == book.short_description
    assert response.data["full_description"] == book.full_description
    assert response.data["last_read_date"] == reading_session.end_time


@pytest.mark.django_db
def test_book_retrieve_not_reading_session_by_authenticated_user(
    auth_client, create_book
):
    book = create_book
    url = reverse("book-detail", args=[book.id])
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == book.id
    assert response.data["title"] == book.title
    assert response.data["author"] == book.author
    assert response.data["year"] == book.year
    assert response.data["short_description"] == book.short_description
    assert response.data["full_description"] == book.full_description
    assert response.data["last_read_date"] is None


@pytest.mark.django_db
def test_book_retrieve_by_unauthenticated_user(client, create_book):
    book = create_book
    url = reverse("book-detail", args=[book.id])
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_book_retrieve_nonexistent_book(auth_client):
    non_id = 0
    url = reverse("book-detail", args=[non_id])
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_start_reading_session_success(auth_client, create_book):
    book = create_book
    url = reverse("start-reading-session", kwargs={"book_id": book.id})
    response = auth_client.post(url)

    assert response.status_code == status.HTTP_201_CREATED
    assert "start_time" in response.data
    assert response.data["book"] == book.id


@pytest.mark.django_db
def test_start_reading_session_unauthenticated_user(client, create_book):
    book = create_book
    url = reverse("start-reading-session", kwargs={"book_id": book.id})
    response = client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_end_non_existent_reading_session(auth_client, create_book):
    book = create_book

    end_session_url = reverse("end-reading-session", kwargs={"book_id": book.id})
    response = auth_client.patch(end_session_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "No active reading session found for this book." in response.data["message"]


@pytest.mark.django_db
def test_end_reading_session_success(
    auth_client, create_book, create_user, start_reading_session
):
    user = create_user
    book = create_book

    start_reading_session(book)

    end_session_url = reverse("end-reading-session", kwargs={"book_id": book.id})
    auth_client.patch(end_session_url)

    reading_session = ReadingSession.objects.get(book=book, user=user)
    assert reading_session.status is False
    assert reading_session.end_time is not None
