import pytest

from library.models import Book, ReadingSession


@pytest.mark.django_db
def test_create_book(create_book):
    assert Book.objects.filter(id=create_book.id).exists()

    assert create_book.title == "Harry Potter and the Philosopher's Stone"
    assert create_book.author == "J. K. Rowling"
    assert create_book.year == 1997
    assert create_book.short_description == "Harry Potter has no idea how famous he is."
    assert create_book.full_description == "..."


@pytest.mark.django_db
def test_book_str(create_book):
    assert str(create_book) == "Harry Potter and the Philosopher's Stone"


@pytest.mark.django_db
def test_create_reading_session(create_reading_session):
    session = create_reading_session
    assert ReadingSession.objects.filter(id=session.id).exists()
    assert session.status is True
    assert session.end_time is None


@pytest.mark.django_db
def test_reading_session_str(create_reading_session):
    session = create_reading_session
    expected_str = f"{session.user.username} - {session.book.title}"
    assert str(session) == expected_str
