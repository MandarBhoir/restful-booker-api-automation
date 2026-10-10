import pytest

from utils.api_client import APIClient
from utils.config_manager import ConfigManager


@pytest.fixture
def api_client():
    """
    Provide an API client configured with the base URL.
    """
    config = ConfigManager()
    return APIClient(config.get_base_url())


@pytest.fixture
def auth_token(api_client):
    """
    Generate an authentication token for authorized API requests.
    """
    payload = {
        "username": "admin",
        "password": "password123"
    }

    response = api_client.post(
        "/auth",
        json=payload
    )

    assert response.status_code == 200, (
        f"Authentication failed: HTTP {response.status_code}"
    )

    response_data = response.json()

    assert "token" in response_data, (
        "Authentication response does not contain a token"
    )

    return response_data["token"]
