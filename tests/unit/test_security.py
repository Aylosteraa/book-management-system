from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

def test_hash_password():
    password = "testpassword123"
    hashed = hash_password(password)

    assert hashed != password

def test_verify_password_success():
    password = "testpassword123"
    hashed = hash_password(password)

    assert verify_password(password, hashed)

def test_verify_password_fail():
    hashed = hash_password("testpassword123")

    assert not verify_password("wrongpassword", hashed)


def test_create_refresh_token():
    token = create_refresh_token(
        {
            "sub": "123"
        }
    )

    payload = decode_token(token)

    assert payload["sub"] == "123"
    assert payload["type"] == "refresh"

def test_decode_invalid_token():
    payload = decode_token(
        "invalid-token"
    )

    assert payload is None