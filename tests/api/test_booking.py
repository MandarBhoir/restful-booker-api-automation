from utils.api_client import APIClient
from utils.config_manager import ConfigManager


def test_get_booking(api_client):

    response = api_client.get("/booking/1")

    assert response.status_code == 200

