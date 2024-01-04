from datetime import timedelta

import django
import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from auth_api.models import UserReadingStats
from library.models import Book, ReadingSession


def pytest_configure():
    if not settings.configured:
        settings.configure(DJANGO_SETTINGS_MODULE="rtas_backend.settings")
    django.setup()


fake = Faker()


@pytest.fixture
def new_user_payload():
    return {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": "password",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(client, create_user):
    access = AccessToken.for_user(create_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client


@pytest.fixture
def create_user(db, new_user_payload):
    return User.objects.create_user(
        username=new_user_payload["username"],
        email=new_user_payload["email"],
        password=new_user_payload["password"],
        first_name=new_user_payload["first_name"],
        last_name=new_user_payload["last_name"],
    )


@pytest.fixture
def create_book(db):
    book = Book.objects.create(
        title="Harry Potter and the Philosopher's Stone",
        author="J. K. Rowling",
        year=1997,
        short_description="Harry Potter has no idea how famous he is.",
        full_description="...",
    )
    return book


@pytest.fixture
def create_reading_session(db, create_book, create_user):
    return ReadingSession.objects.create(
        user=create_user, book=create_book, start_time=timezone.now(), status=True
    )


@pytest.fixture
def end_reading_session(db, create_book, create_user):
    return ReadingSession.objects.create(
        user=create_user, book=create_book, start_time=timezone.now(), status=False
    )


@pytest.fixture
def start_reading_session(auth_client, create_book):
    def start_session(book):
        url = reverse("start-reading-session", kwargs={"book_id": book.id})
        return auth_client.post(url)

    return start_session


@pytest.fixture
def reading_session(db, create_user, create_book):
    start_time = timezone.now()
    end_time = start_time + timedelta(hours=1)
    return ReadingSession.objects.create(
        user=create_user, book=create_book, start_time=start_time, end_time=end_time
    )


@pytest.fixture
def user_reading_stats(db, create_user):
    user = create_user
    user_stats, created = UserReadingStats.objects.get_or_create(
        user=user,
        defaults={
            "statistic_time_7_days": timedelta(days=7),
            "statistic_time_30_days": timedelta(days=30),
        },
    )

    if not created:
        user_stats.statistic_time_7_days = timedelta(days=7)
        user_stats.statistic_time_30_days = timedelta(days=30)
        user_stats.save()

    return user_stats


@pytest.fixture
def create_reading_sessions(create_user, create_book):
    def _create_sessions(days_before_now, duration_hours, number_of_users=2):
        users = [create_user for _ in range(number_of_users)]
        book = create_book
        now = timezone.now()

        for user in users:
            start_time = now - timedelta(days=days_before_now)
            end_time = start_time + timedelta(hours=duration_hours)
            ReadingSession.objects.create(
                user=user, book=book, start_time=start_time, end_time=end_time
            )

        return users

    return _create_sessions
