import pytest

from library.serializers import BookListSerializer, BookRetrieveSerializer, StartReadingSessionSerializer


@pytest.mark.django_db
def test_book_list_serializer(create_book):
    book = create_book

    serializer = BookListSerializer(book)
    data = serializer.data

    assert set(data.keys()) == {"id", "title", "author", "year", "short_description"}
    assert data["title"] == book.title
    assert data["author"] == book.author
    assert data["year"] == book.year
    assert data["short_description"] == book.short_description


@pytest.mark.django_db
def test_book_retrieve_serializer_with_reading_session(
    create_book, create_user, create_reading_session
):
    reading_session = create_reading_session
    book = create_book
    serializer = BookRetrieveSerializer(book)
    data = serializer.data

    assert set(data.keys()) == {
        "id",
        "title",
        "author",
        "year",
        "short_description",
        "full_description",
        "last_read_date",
    }
    assert data["last_read_date"] == reading_session.end_time


@pytest.mark.django_db
def test_book_retrieve_serializer_without_reading_session(create_book):
    book = create_book
    serializer = BookRetrieveSerializer(book)
    data = serializer.data

    assert data["last_read_date"] is None


@pytest.mark.django_db
def test_start_reading_session_serializer_serialization(create_reading_session):
    reading_session = create_reading_session
    serializer = StartReadingSessionSerializer(reading_session)
    data = serializer.data

    assert set(data.keys()) == {"user", "book", "start_time"}
    assert data["user"] == reading_session.user.id
    assert data["book"] == reading_session.book.id
    assert data["start_time"] is not None


@pytest.mark.django_db
def test_start_reading_session_serializer_deserialization(
    create_user, create_book, create_reading_session
):
    serializer = StartReadingSessionSerializer(
        data={
            "user": create_reading_session.user.id,
            "book": create_reading_session.book.id,
            "start_time": create_reading_session.start_time,
        }
    )

    assert serializer.is_valid()
    reading_session = serializer.save()

    assert reading_session.user == create_reading_session.user
    assert reading_session.book == create_reading_session.book
    assert reading_session.start_time is not None
