import pytest

from tests.test_data.booking_data import get_booking_data
from utils.booking_helper import create_booking, delete_booking


# ============================================================
# 1. Positive Scenarios
# ============================================================

def test_delete_existing_booking(api_client, auth_token):
    booking_id = create_booking(api_client)

    response = delete_booking(api_client, booking_id, auth_token)

    assert response.status_code == 201


def test_delete_booking_and_verify_not_found(api_client, auth_token):
    booking_id = create_booking(api_client)

    delete_response = delete_booking(api_client, booking_id, auth_token)

    assert delete_response.status_code == 201

    get_response = api_client.get(f"/booking/{booking_id}")

    assert get_response.status_code == 404


def test_delete_booking_with_valid_authentication(api_client, auth_token):
    booking_id = create_booking(api_client)

    response = delete_booking(api_client, booking_id, auth_token)

    assert response.status_code == 201


# ============================================================
# 2. Authentication Scenarios
# ============================================================

def test_delete_booking_without_authentication(api_client):
    booking_id = create_booking(api_client)

    response = api_client.delete(f"/booking/{booking_id}")

    assert response.status_code in [401, 403]

    get_response = api_client.get(f"/booking/{booking_id}")
    assert get_response.status_code == 200


def test_delete_booking_with_invalid_token(api_client):
    booking_id = create_booking(api_client)

    response = api_client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": "token=invalid-token"}
    )

    assert response.status_code in [401, 403]

    get_response = api_client.get(f"/booking/{booking_id}")
    assert get_response.status_code == 200


def test_delete_booking_with_malformed_token(api_client):
    booking_id = create_booking(api_client)

    response = api_client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": "invalid-token"}
    )

    assert response.status_code in [401, 403]

    get_response = api_client.get(f"/booking/{booking_id}")
    assert get_response.status_code == 200


# ============================================================
# 3. Invalid Booking ID Scenarios
# ============================================================

@pytest.mark.parametrize(
    "booking_id",
    [999999999, 0, -1, -999]
)
def test_delete_booking_with_invalid_numeric_id(
    api_client, auth_token, booking_id
):
    response = delete_booking(api_client, booking_id, auth_token)

    assert response.status_code != 201


@pytest.mark.parametrize(
    "booking_id",
    ["invalid", "abc", "test-id"]
)
def test_delete_booking_with_invalid_id_format(
    api_client, auth_token, booking_id
):
    response = delete_booking(api_client, booking_id, auth_token)

    assert response.status_code != 201


# ============================================================
# 4. Delete Lifecycle Scenarios
# ============================================================

def test_delete_same_booking_twice(api_client, auth_token):
    booking_id = create_booking(api_client)

    first_delete = delete_booking(api_client, booking_id, auth_token)
    assert first_delete.status_code == 201

    second_delete = delete_booking(api_client, booking_id, auth_token)
    assert second_delete.status_code != 201


def test_create_update_delete_get_booking(api_client, auth_token):
    booking_id = create_booking(api_client)

    updated_data = get_booking_data()
    updated_data["firstname"] = "BeforeDelete"
    updated_data["totalprice"] = 500

    update_response = api_client.put(
        f"/booking/{booking_id}",
        json=updated_data,
        headers={"Cookie": f"token={auth_token}"}
    )

    assert update_response.status_code == 200

    delete_response = delete_booking(api_client, booking_id, auth_token)
    assert delete_response.status_code == 201

    get_response = api_client.get(f"/booking/{booking_id}")
    assert get_response.status_code == 404


def test_delete_one_booking_does_not_affect_another(api_client, auth_token):
    first_booking_id = create_booking(api_client)
    second_booking_id = create_booking(api_client)

    delete_response = delete_booking(
        api_client, first_booking_id, auth_token
    )
    assert delete_response.status_code == 201

    first_get = api_client.get(f"/booking/{first_booking_id}")
    second_get = api_client.get(f"/booking/{second_booking_id}")

    assert first_get.status_code == 404
    assert second_get.status_code == 200


def test_delete_multiple_bookings(api_client, auth_token):
    booking_ids = [
        create_booking(api_client),
        create_booking(api_client),
        create_booking(api_client)
    ]

    for booking_id in booking_ids:
        response = delete_booking(api_client, booking_id, auth_token)
        assert response.status_code == 201

    for booking_id in booking_ids:
        response = api_client.get(f"/booking/{booking_id}")
        assert response.status_code == 404


# ============================================================
# 5. Data Integrity / Response Validation
# ============================================================

def test_delete_response_status_code(api_client, auth_token):
    booking_id = create_booking(api_client)

    response = delete_booking(api_client, booking_id, auth_token)

    assert response.status_code == 201


def test_delete_response_body(api_client, auth_token):
    booking_id = create_booking(api_client)

    response = delete_booking(api_client, booking_id, auth_token)

    assert response.status_code == 201
    assert response.text == "Created"


def test_deleted_booking_cannot_be_retrieved(api_client, auth_token):
    booking_id = create_booking(api_client)

    delete_response = delete_booking(api_client, booking_id, auth_token)
    assert delete_response.status_code == 201

    get_response = api_client.get(f"/booking/{booking_id}")
    assert get_response.status_code == 404


# ============================================================
# 6. End-to-End Lifecycle
# ============================================================

def test_create_get_delete_get(api_client, auth_token):
    booking_id = create_booking(api_client)

    get_before_delete = api_client.get(f"/booking/{booking_id}")
    assert get_before_delete.status_code == 200

    delete_response = delete_booking(api_client, booking_id, auth_token)
    assert delete_response.status_code == 201

    get_after_delete = api_client.get(f"/booking/{booking_id}")
    assert get_after_delete.status_code == 404


def test_create_update_delete_lifecycle(api_client, auth_token):
    booking_id = create_booking(api_client)

    updated_data = get_booking_data()
    updated_data["firstname"] = "DeleteLifecycle"
    updated_data["lastname"] = "TestUser"

    update_response = api_client.put(
        f"/booking/{booking_id}",
        json=updated_data,
        headers={"Cookie": f"token={auth_token}"}
    )

    assert update_response.status_code == 200

    get_response = api_client.get(f"/booking/{booking_id}")
    assert get_response.status_code == 200
    assert get_response.json()["firstname"] == "DeleteLifecycle"

    delete_response = delete_booking(api_client, booking_id, auth_token)
    assert delete_response.status_code == 201

    final_get_response = api_client.get(f"/booking/{booking_id}")
    assert final_get_response.status_code == 404
