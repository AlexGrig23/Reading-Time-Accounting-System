import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from auth_api.models import UserReadingStats


@pytest.mark.django_db(transaction=True)
def test_signup(client, new_user_payload):
    """
    Test sign up with valid data and check create user and user reading stats
    """
    url = reverse("sign-up")
    response = client.post(url, new_user_payload)
    data = response.data

    assert response.status_code == status.HTTP_201_CREATED

    assert data["username"] == new_user_payload["username"]
    assert data["email"] == new_user_payload["email"]
    assert data["first_name"] == new_user_payload["first_name"]
    assert data["last_name"] == new_user_payload["last_name"]
    assert "password" not in data

    user = User.objects.get(username=new_user_payload["username"])
    assert UserReadingStats.objects.filter(user=user).exists()


@pytest.mark.django_db(transaction=True)
def test_signup_with_invalid_email(client, new_user_payload):
    new_user_payload["email"] = "invalid-email"
    url = reverse("sign-up")
    response = client.post(url, new_user_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db(transaction=True)
def test_signup_with_existing_email(client, create_user, new_user_payload):
    new_user_payload["email"] = create_user.email
    url = reverse("sign-up")
    response = client.post(url, new_user_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db(transaction=True)
def test_signup_with_existing_username(client, create_user, new_user_payload):
    new_user_payload["username"] = create_user.username
    url = reverse("sign-up")
    response = client.post(url, new_user_payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db(transaction=True)
def test_signup_password_hashing(client, new_user_payload):
    url = reverse("sign-up")
    response = client.post(url, new_user_payload)

    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(username=new_user_payload["username"])
    assert user.check_password(new_user_payload["password"])
