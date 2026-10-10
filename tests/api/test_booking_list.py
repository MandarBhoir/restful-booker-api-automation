import pytest

from tests.test_data.booking_data import get_booking_data


# ============================================================
# Helper Functions
# ============================================================

def create_booking(api_client, booking_data=None):
    if booking_data is None:
        booking_data = get_booking_data()

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code == 200
    return response.json()["bookingid"]


def get_all_bookings(api_client):
    return api_client.get("/booking")


# ============================================================
# 1. Basic Collection Endpoint
# ============================================================

def test_get_all_bookings(api_client):
    response = get_all_bookings(api_client)
    assert response.status_code == 200


def test_get_all_bookings_returns_list(api_client):
    response = get_all_bookings(api_client)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_bookings_contains_booking_records(api_client):
    response = get_all_bookings(api_client)

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) > 0
    assert isinstance(response_data[0], dict)


def test_booking_list_contains_booking_id(api_client):
    response = get_all_bookings(api_client)

    assert response.status_code == 200

    for booking in response.json():
        assert "bookingid" in booking
        assert isinstance(booking["bookingid"], int)


# ============================================================
# 2. Create Booking and Verify in List
# ============================================================

def test_created_booking_appears_in_booking_list(api_client):
    booking_id = create_booking(api_client)

    response = get_all_bookings(api_client)

    assert response.status_code == 200

    booking_ids = [
        booking["bookingid"]
        for booking in response.json()
    ]

    assert booking_id in booking_ids


def test_multiple_created_bookings_appear_in_list(api_client):
    first_booking_id = create_booking(api_client)
    second_booking_id = create_booking(api_client)

    response = get_all_bookings(api_client)

    assert response.status_code == 200

    booking_ids = [
        booking["bookingid"]
        for booking in response.json()
    ]

    assert first_booking_id in booking_ids
    assert second_booking_id in booking_ids


# ============================================================
# 3. Filter by First Name
# ============================================================

def test_filter_booking_by_firstname(api_client):
    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = api_client.get(
        "/booking",
        params={"firstname": booking_data["firstname"]}
    )

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_filter_booking_by_non_existing_firstname(api_client):
    response = api_client.get(
        "/booking",
        params={"firstname": "ThisNameDoesNotExist12345"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_booking_with_empty_firstname(api_client):
    response = api_client.get(
        "/booking",
        params={"firstname": ""}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# 4. Filter by Last Name
# ============================================================

def test_filter_booking_by_lastname(api_client):
    booking_data = get_booking_data()
    create_booking(api_client, booking_data)

    response = api_client.get(
        "/booking",
        params={"lastname": booking_data["lastname"]}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_booking_by_non_existing_lastname(api_client):
    response = api_client.get(
        "/booking",
        params={"lastname": "ThisLastNameDoesNotExist12345"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_booking_with_empty_lastname(api_client):
    response = api_client.get(
        "/booking",
        params={"lastname": ""}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# 5. Combined Name Filters
# ============================================================

def test_filter_booking_by_firstname_and_lastname(api_client):
    booking_data = get_booking_data()
    create_booking(api_client, booking_data)

    response = api_client.get(
        "/booking",
        params={
            "firstname": booking_data["firstname"],
            "lastname": booking_data["lastname"]
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_booking_with_mismatched_name_combination(api_client):
    booking_data = get_booking_data()

    response = api_client.get(
        "/booking",
        params={
            "firstname": booking_data["firstname"],
            "lastname": "NonExistingLastName12345"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ============================================================
# 6. Date Filters
# ============================================================

def test_filter_booking_by_checkin_date(api_client):
    booking_data = get_booking_data()
    create_booking(api_client, booking_data)

    response = api_client.get(
        "/booking",
        params={
            "checkin": booking_data["bookingdates"]["checkin"]
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_booking_by_checkout_date(api_client):
    booking_data = get_booking_data()
    create_booking(api_client, booking_data)

    response = api_client.get(
        "/booking",
        params={
            "checkout": booking_data["bookingdates"]["checkout"]
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_booking_by_invalid_checkin_date(api_client):
    response = api_client.get(
        "/booking",
        params={"checkin": "invalid-date"}
    )

    assert response.status_code == 500
    assert response.text == "Internal Server Error"


def test_filter_booking_by_invalid_checkout_date(api_client):
    response = api_client.get(
        "/booking",
        params={"checkout": "invalid-date"}
    )

    assert response.status_code == 500
    assert response.text == "Internal Server Error"


# ============================================================
# 7. Response Structure Validation
# ============================================================

def test_booking_list_response_structure(api_client):
    response = get_all_bookings(api_client)

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)

    for booking in response_data:
        assert isinstance(booking, dict)
        assert "bookingid" in booking
        assert isinstance(booking["bookingid"], int)


def test_booking_list_does_not_return_empty_booking_objects(api_client):
    response = get_all_bookings(api_client)

    assert response.status_code == 200

    for booking in response.json():
        assert booking != {}


def test_booking_ids_are_unique(api_client):
    response = get_all_bookings(api_client)

    assert response.status_code == 200

    booking_ids = [
        booking["bookingid"]
        for booking in response.json()
    ]

    assert len(booking_ids) == len(set(booking_ids))


# ============================================================
# 8. End-to-End Filtering Scenarios
# ============================================================

def test_create_filter_validate_booking(api_client):
    booking_data = get_booking_data()
    booking_data["firstname"] = "ListTestFirst"
    booking_data["lastname"] = "ListTestLast"

    create_booking(api_client, booking_data)

    response = api_client.get(
        "/booking",
        params={
            "firstname": "ListTestFirst",
            "lastname": "ListTestLast"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_multiple_bookings_and_filter(api_client):
    first_data = get_booking_data()
    first_data["firstname"] = "FilterFirstA"

    second_data = get_booking_data()
    second_data["firstname"] = "FilterFirstB"

    create_booking(api_client, first_data)
    create_booking(api_client, second_data)

    response = api_client.get(
        "/booking",
        params={"firstname": "FilterFirstA"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for booking in response.json():
        assert "bookingid" in booking


def test_create_filter_delete_verify(api_client, auth_token):
    booking_data = get_booking_data()
    booking_data["firstname"] = "DeleteFilterTest"

    booking_id = create_booking(api_client, booking_data)

    filter_response = api_client.get(
        "/booking",
        params={"firstname": "DeleteFilterTest"}
    )

    assert filter_response.status_code == 200
    assert isinstance(filter_response.json(), list)

    delete_response = api_client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )

    assert delete_response.status_code == 201

    get_response = api_client.get(f"/booking/{booking_id}")
    assert get_response.status_code == 404