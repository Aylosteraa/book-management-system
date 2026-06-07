import uuid

import pytest


@pytest.mark.asyncio
async def test_register_user(client):

    email = f"{uuid.uuid4()}@example.com"

    response = await client.post(
        "/user/register",
        json={
            "email": email,
            "password": "Password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == email


@pytest.mark.asyncio
async def test_register_duplicate_email(client):

    email = f"{uuid.uuid4()}@example.com"

    payload = {
        "email": email,
        "password": "Password123"
    }

    await client.post(
        "/user/register",
        json=payload
    )

    response = await client.post(
        "/user/register",
        json=payload
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client):

    email = f"{uuid.uuid4()}@example.com"

    await client.post(
        "/user/register",
        json={
            "email": email,
            "password": "Password123"
        }
    )

    response = await client.post(
        "/user/login",
        json={
            "email": email,
            "password": "Password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client):

    email = f"{uuid.uuid4()}@example.com"

    await client.post(
        "/user/register",
        json={
            "email": email,
            "password": "Password123"
        }
    )

    response = await client.post(
        "/user/login",
        json={
            "email": email,
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):

    email = f"{uuid.uuid4()}@example.com"

    await client.post(
        "/user/register",
        json={
            "email": email,
            "password": "Password123"
        }
    )

    login_response = await client.post(
        "/user/login",
        json={
            "email": email,
            "password": "Password123"
        }
    )

    refresh_token = login_response.json()["refresh_token"]

    response = await client.post(
        "/user/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data