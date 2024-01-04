import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_book_reading_time_list_view_authenticated_user(
    auth_client, create_user, create_book, reading_session
):
    url = reverse("books-statistic")
    response = auth_client.get(url)
    data = response.data

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(data, list)

    book_data = next((book for book in data if book["id"] == create_book.id), None)
    assert book_data is not None
    assert book_data["title"] == create_book.title
    assert book_data["author"] == create_book.author
    assert book_data["total_reading_time"] is not None


@pytest.mark.django_db
def test_book_reading_time_list_view_unauthenticated_user(client):
    url = reverse("books-statistic")
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_book_reading_time_retrieve_view_authenticated_user(
    auth_client, create_book, reading_session
):
    url = reverse("books-retrieve-statistic", kwargs={"pk": create_book.id})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == create_book.id
    assert response.data["title"] == create_book.title
    assert response.data["author"] == create_book.author
    assert "total_reading_time" in response.data


@pytest.mark.django_db
def test_book_reading_time_retrieve_view_unauthenticated_user(client, create_book):
    url = reverse("books-retrieve-statistic", kwargs={"pk": create_book.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_book_reading_time_retrieve_view_nonexistent_book(auth_client):
    non_book_id = 0
    url = reverse("books-retrieve-statistic", kwargs={"pk": non_book_id})
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_book_reading_time_list_view_authenticated_user(
    auth_client, create_user, create_book, reading_session
):
    url = reverse("users-statistic")
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert "username" in data
    assert data["username"] == create_user.username
    assert "statistics" in data
    assert "statistic_time_7_days" in data["statistics"]
    assert "statistic_time_30_days" in data["statistics"]
    assert "books" in data
    assert isinstance(data["books"], list)

    book_data = next(
        (book for book in data["books"] if book["id"] == create_book.id), None
    )
    assert book_data is not None
    assert book_data["title"] == create_book.title
    assert book_data["author"] == create_book.author
    assert "total_reading_time" in book_data
    assert book_data["total_reading_time"] is not None


@pytest.mark.django_db
def test_user_book_reading_time_list_view_unauthenticated_user(client):
    url = reverse("users-statistic")
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
