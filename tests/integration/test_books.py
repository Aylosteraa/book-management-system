import io

import pytest

from app.core.dependencies import get_current_user
from app.main import app
from app.models.user_model import User


@pytest.fixture
def mock_user():

    async def override_current_user():
        return User(
            email="test@test.com",
            password_hash="hash"
        )

    app.dependency_overrides[get_current_user] = override_current_user

    yield

    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_create_book(client, mock_user):

    response = await client.post(
        "/books/",
        json={
            "title": "Clean Code",
            "author": "Robert Martin",
            "genre": "sci_fi",
            "year": 2008,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Clean Code"
    assert data["author"] == "Robert Martin"


@pytest.mark.asyncio
async def test_list_books(client, mock_user):

    await client.post(
        "/books/",
        json={
            "title": "Book One",
            "author": "Author One",
            "genre": "sci_fi",
            "year": 2024,
        },
    )

    response = await client.get("/books/")

    assert response.status_code == 200

    data = response.json()

    assert "books" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_get_book(client, mock_user):

    created = await client.post(
        "/books/",
        json={
            "title": "Domain Driven Design",
            "author": "Eric Evans",
            "genre": "sci_fi",
            "year": 2003,
        },
    )

    book_id = created.json()["id"]

    response = await client.get(f"/books/{book_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == book_id
    assert data["title"] == "Domain Driven Design"


@pytest.mark.asyncio
async def test_update_book(client, mock_user):

    created = await client.post(
        "/books/",
        json={
            "title": "Old Title",
            "author": "Author",
            "genre": "sci_fi",
            "year": 2020,
        },
    )

    book_id = created.json()["id"]

    response = await client.patch(
        f"/books/{book_id}",
        json={
            "title": "New Title"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New Title"


@pytest.mark.asyncio
async def test_delete_book(client, mock_user):

    created = await client.post(
        "/books/",
        json={
            "title": "Delete Me",
            "author": "Author",
            "genre": "sci_fi",
            "year": 2020,
        },
    )

    book_id = created.json()["id"]

    response = await client.delete(f"/books/{book_id}")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_nonexistent_book(client):

    response = await client.get(
        "/books/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_export_books(client, mock_user):

    response = await client.get("/books/export")

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_import_books(client, mock_user):

    csv_content = (
        "title,author,genre,year\n"
        "Python Book,John Doe,sci_fi,2024\n"
    )

    files = {
        "file": (
            "books.csv",
            io.BytesIO(csv_content.encode("utf-8")),
            "text/csv",
        )
    }

    response = await client.post(
        "/books/import",
        files=files,
    )

    assert response.status_code == 200

    data = response.json()

    assert "imported" in data
    assert "failed" in data
    assert "skipped" in data