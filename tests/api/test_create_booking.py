
import pytest

from tests.test_data.booking_data import get_booking_data


# ============================================================
# Positive Scenarios
# ============================================================

@pytest.mark.smoke
def test_create_booking(api_client):
    """Smoke test: verify that a booking can be created successfully."""

    booking_data = get_booking_data()

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "bookingid" in response_data
    assert "booking" in response_data

    booking = response_data["booking"]

    assert booking["firstname"] == booking_data["firstname"]
    assert booking["lastname"] == booking_data["lastname"]
    assert booking["totalprice"] == booking_data["totalprice"]
    assert booking["depositpaid"] == booking_data["depositpaid"]
    assert booking["bookingdates"] == booking_data["bookingdates"]
    assert booking["additionalneeds"] == booking_data["additionalneeds"]


@pytest.mark.parametrize(
    "deposit_paid",
    [True, False]
)
def test_create_booking_with_deposit_status(api_client, deposit_paid):

    booking_data = get_booking_data()
    booking_data["depositpaid"] = deposit_paid

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "bookingid" in response_data
    assert response_data["booking"]["depositpaid"] == deposit_paid


def test_create_booking_without_additional_needs(api_client):

    booking_data = get_booking_data()
    booking_data.pop("additionalneeds")

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "bookingid" in response_data
    assert response_data["booking"]["firstname"] == booking_data["firstname"]


def test_create_booking_with_different_dates(api_client):

    booking_data = get_booking_data()

    booking_data["bookingdates"] = {
        "checkin": "2027-01-10",
        "checkout": "2027-01-20"
    }

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["booking"]["bookingdates"] == booking_data["bookingdates"]


# ============================================================
# Negative Scenarios - Missing Required Fields
# ============================================================

@pytest.mark.parametrize(
    "field",
    [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates"
    ]
)
def test_create_booking_missing_required_field(api_client, field):

    booking_data = get_booking_data()
    booking_data.pop(field)

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    # Restful Booker behavior for missing required fields.
    assert response.status_code != 200


def test_create_booking_missing_checkin(api_client):

    booking_data = get_booking_data()

    booking_data["bookingdates"] = {
        "checkout": "2026-10-15"
    }

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code != 200


def test_create_booking_missing_checkout(api_client):

    booking_data = get_booking_data()

    booking_data["bookingdates"] = {
        "checkin": "2026-10-10"
    }

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code != 200


def test_create_booking_empty_body(api_client):

    response = api_client.post(
        "/booking",
        json={}
    )

    assert response.status_code != 200


# ============================================================
# API Behavior / Data Type Scenarios
# ============================================================

@pytest.mark.parametrize(
    "field,value",
    [
        ("firstname", ""),
        ("lastname", ""),
        ("depositpaid", "true"),
        ("totalprice", "150")
    ]
)
def test_create_booking_with_accepted_invalid_data(
    api_client,
    field,
    value
):

    booking_data = get_booking_data()
    booking_data[field] = value

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    # Current Restful Booker behavior:
    # These values are accepted and return HTTP 200.
    assert response.status_code == 200

    response_data = response.json()

    assert "bookingid" in response_data
    assert "booking" in response_data


# ============================================================
# Response Validation
# ============================================================

def test_create_booking_response_contains_booking_id(api_client):

    booking_data = get_booking_data()

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "bookingid" in response_data
    assert isinstance(response_data["bookingid"], int)


def test_create_booking_response_contains_booking_object(api_client):

    booking_data = get_booking_data()

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "booking" in response_data
    assert isinstance(response_data["booking"], dict)


@pytest.mark.sanity
def test_create_booking_response_matches_request(api_client):
    """Sanity test: verify that the created booking matches the request."""

    booking_data = get_booking_data()

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code == 200

    response_data = response.json()
    booking = response_data["booking"]

    assert booking["firstname"] == booking_data["firstname"]
    assert booking["lastname"] == booking_data["lastname"]
    assert booking["totalprice"] == booking_data["totalprice"]
    assert booking["depositpaid"] == booking_data["depositpaid"]
    assert booking["bookingdates"] == booking_data["bookingdates"]
    assert booking["additionalneeds"] == booking_data["additionalneeds"]
