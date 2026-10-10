
import pytest


@pytest.mark.smoke
def test_create_auth_token(api_client):
    """Smoke test: verify that the API can generate an auth token."""

    payload = {
        "username": "admin",
        "password": "password123"
    }

    response = api_client.post(
        "/auth",
        json=payload
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "token" in response_data
    assert response_data["token"]


@pytest.mark.parametrize(
    "payload",
    [
        {
            "username": "invalid_user",
            "password": "password123"
        },
        {
            "username": "admin",
            "password": "invalid_password"
        },
        {
            "username": "invalid_user",
            "password": "invalid_password"
        },
        {
            "password": "password123"
        },
        {
            "username": "admin"
        },
        {
            "username": "",
            "password": ""
        }
    ]
)
def test_invalid_authentication(api_client, payload):
    """Verify that invalid credentials do not generate an auth token."""

    response = api_client.post(
        "/auth",
        json=payload
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "token" not in response_data
    assert "reason" in response_data
    assert response_data["reason"] == "Bad credentials"
