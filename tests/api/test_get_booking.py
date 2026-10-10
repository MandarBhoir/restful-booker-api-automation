import pytest

from tests.test_data.booking_data import get_booking_data
from utils.booking_helper import create_booking, get_booking


# ============================================================
# Positive Scenarios
# ============================================================

def test_get_existing_booking(api_client):

    booking_id = create_booking(api_client)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200


def test_get_booking_after_creation(api_client):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["firstname"] == booking_data["firstname"]
    assert response_data["lastname"] == booking_data["lastname"]


# ============================================================
# Response Data Validation
# ============================================================

def test_get_booking_firstname(api_client):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200
    assert response.json()["firstname"] == booking_data["firstname"]


def test_get_booking_lastname(api_client):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200
    assert response.json()["lastname"] == booking_data["lastname"]


def test_get_booking_totalprice(api_client):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200
    assert response.json()["totalprice"] == booking_data["totalprice"]


def test_get_booking_depositpaid(api_client):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200
    assert response.json()["depositpaid"] == booking_data["depositpaid"]


def test_get_booking_dates(api_client):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200
    assert response.json()["bookingdates"] == booking_data["bookingdates"]


def test_get_booking_additional_needs(api_client):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200
    assert response.json()["additionalneeds"] == booking_data["additionalneeds"]


# ============================================================
# Response Structure / Data Type Validation
# ============================================================

def test_get_booking_response_is_json_object(api_client):

    booking_id = create_booking(api_client)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_booking_contains_expected_fields(api_client):

    booking_id = create_booking(api_client)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200

    response_data = response.json()

    expected_fields = {
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
        "additionalneeds"
    }

    assert expected_fields.issubset(response_data.keys())


def test_get_booking_field_data_types(api_client):

    booking_id = create_booking(api_client)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data["firstname"], str)
    assert isinstance(response_data["lastname"], str)
    assert isinstance(response_data["totalprice"], int)
    assert isinstance(response_data["depositpaid"], bool)
    assert isinstance(response_data["bookingdates"], dict)
    assert isinstance(response_data["additionalneeds"], str)


def test_get_booking_date_structure(api_client):

    booking_id = create_booking(api_client)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200

    booking_dates = response.json()["bookingdates"]

    assert "checkin" in booking_dates
    assert "checkout" in booking_dates

    assert isinstance(booking_dates["checkin"], str)
    assert isinstance(booking_dates["checkout"], str)


def test_get_booking_date_values(api_client):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200

    booking_dates = response.json()["bookingdates"]

    assert booking_dates["checkin"] == booking_data["bookingdates"]["checkin"]
    assert booking_dates["checkout"] == booking_data["bookingdates"]["checkout"]


# ============================================================
# Negative Scenarios
# ============================================================

@pytest.mark.parametrize(
    "booking_id",
    [
        999999999,
        0,
        -1,
        -999
    ]
)
def test_get_booking_with_invalid_numeric_id(api_client, booking_id):

    response = get_booking(api_client, booking_id)

    assert response.status_code != 200


@pytest.mark.parametrize(
    "booking_id",
    [
        "invalid",
        "abc",
        "test-id"
    ]
)
def test_get_booking_with_invalid_id_format(api_client, booking_id):

    response = get_booking(api_client, booking_id)

    assert response.status_code != 200


# ============================================================
# Data Integrity / Consistency
# ============================================================

def test_get_booking_data_matches_created_booking(api_client):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = get_booking(api_client, booking_id)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["firstname"] == booking_data["firstname"]
    assert response_data["lastname"] == booking_data["lastname"]
    assert response_data["totalprice"] == booking_data["totalprice"]
    assert response_data["depositpaid"] == booking_data["depositpaid"]
    assert response_data["bookingdates"] == booking_data["bookingdates"]
    assert response_data["additionalneeds"] == booking_data["additionalneeds"]


def test_get_same_booking_twice_returns_consistent_data(api_client):

    booking_id = create_booking(api_client)

    first_response = get_booking(api_client, booking_id)
    second_response = get_booking(api_client, booking_id)

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    assert first_response.json() == second_response.json()


def test_get_booking_after_update(api_client, auth_token):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    updated_booking = get_booking_data()
    updated_booking["firstname"] = "UpdatedMandar"
    updated_booking["totalprice"] = 500

    update_response = api_client.put(
        f"/booking/{booking_id}",
        json=updated_booking,
        headers={
            "Cookie": f"token={auth_token}"
        }
    )

    assert update_response.status_code == 200

    get_response = get_booking(api_client, booking_id)

    assert get_response.status_code == 200

    response_data = get_response.json()

    assert response_data["firstname"] == "UpdatedMandar"
    assert response_data["totalprice"] == 500


def test_get_booking_after_delete(api_client, auth_token):

    booking_id = create_booking(api_client)

    delete_response = api_client.delete(
        f"/booking/{booking_id}",
        headers={
            "Cookie": f"token={auth_token}"
        }
    )

    assert delete_response.status_code == 201

    get_response = get_booking(api_client, booking_id)

    assert get_response.status_code == 404
