import pytest

from tests.test_data.booking_data import get_booking_data
from utils.booking_helper import create_booking, update_booking


# ============================================================
# Helper Functions
# ============================================================

def get_updated_booking_data():
    return {
        "firstname": "UpdatedMandar",
        "lastname": "UpdatedBhoir",
        "totalprice": 500,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-11-01",
            "checkout": "2026-11-10"
        },
        "additionalneeds": "Lunch"
    }


# ============================================================
# 1. Positive Scenarios
# ============================================================

def test_update_existing_booking(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200


def test_update_firstname(api_client, auth_token):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    updated_data = get_booking_data()
    updated_data["firstname"] = "UpdatedFirstName"

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["firstname"] == updated_data["firstname"]


def test_update_lastname(api_client, auth_token):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    updated_data = get_booking_data()
    updated_data["lastname"] = "UpdatedLastName"

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["lastname"] == updated_data["lastname"]


def test_update_totalprice(api_client, auth_token):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    updated_data = get_booking_data()
    updated_data["totalprice"] = 999

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["totalprice"] == updated_data["totalprice"]


def test_update_depositpaid(api_client, auth_token):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    updated_data = get_booking_data()
    updated_data["depositpaid"] = False

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["depositpaid"] is updated_data["depositpaid"]


def test_update_bookingdates(api_client, auth_token):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    updated_data = get_booking_data()
    updated_data["bookingdates"] = {
        "checkin": "2027-01-01",
        "checkout": "2027-01-10"
    }

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["bookingdates"] == updated_data["bookingdates"]


def test_update_additionalneeds(api_client, auth_token):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    updated_data = get_booking_data()
    updated_data["additionalneeds"] = "Dinner"

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["additionalneeds"] == updated_data["additionalneeds"]


def test_update_all_booking_fields(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data == updated_data


def test_get_booking_after_update(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    update_response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert update_response.status_code == 200

    get_response = api_client.get(f"/booking/{booking_id}")

    assert get_response.status_code == 200
    assert get_response.json() == updated_data


def test_update_same_booking_twice(api_client, auth_token):

    booking_id = create_booking(api_client)

    first_update = get_booking_data()
    first_update["firstname"] = "FirstUpdate"

    second_update = get_booking_data()
    second_update["firstname"] = "SecondUpdate"

    first_response = update_booking(
        api_client, booking_id, auth_token, first_update
    )

    second_response = update_booking(
        api_client, booking_id, auth_token, second_update
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["firstname"] == "SecondUpdate"


# ============================================================
# 2. Updated Data Validation
# ============================================================

def test_updated_firstname_is_correct(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["firstname"] == updated_data["firstname"]


def test_updated_lastname_is_correct(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["lastname"] == updated_data["lastname"]


def test_updated_totalprice_is_correct(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["totalprice"] == updated_data["totalprice"]


def test_updated_depositpaid_is_correct(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["depositpaid"] == updated_data["depositpaid"]


def test_updated_bookingdates_are_correct(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["bookingdates"] == updated_data["bookingdates"]


def test_updated_additionalneeds_is_correct(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200
    assert response.json()["additionalneeds"] == updated_data["additionalneeds"]


def test_updated_response_contains_all_fields(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200

    expected_fields = {
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
        "additionalneeds"
    }

    assert expected_fields.issubset(response.json().keys())


def test_updated_response_field_types(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data["firstname"], str)
    assert isinstance(response_data["lastname"], str)
    assert isinstance(response_data["totalprice"], int)
    assert isinstance(response_data["depositpaid"], bool)
    assert isinstance(response_data["bookingdates"], dict)
    assert isinstance(response_data["additionalneeds"], str)


# ============================================================
# 3. Authentication Scenarios
# ============================================================

def test_update_with_valid_authentication(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200


def test_update_without_authentication(api_client):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = api_client.put(
        f"/booking/{booking_id}",
        json=updated_data
    )

    assert response.status_code in [401, 403]


def test_update_with_invalid_token(api_client):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = api_client.put(
        f"/booking/{booking_id}",
        json=updated_data,
        headers={"Cookie": "token=invalid-token"}
    )

    assert response.status_code in [401, 403]


def test_update_with_malformed_token(api_client):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    response = api_client.put(
        f"/booking/{booking_id}",
        json=updated_data,
        headers={"Cookie": "invalid-token"}
    )

    assert response.status_code in [401, 403]


# ============================================================
# 4. Invalid Booking ID Scenarios
# ============================================================

@pytest.mark.parametrize(
    "booking_id",
    [999999999, 0, -1, -999]
)
def test_update_with_invalid_numeric_booking_id(
    api_client, auth_token, booking_id
):

    updated_data = get_updated_booking_data()

    response = update_booking(
        api_client, booking_id, auth_token, updated_data
    )

    assert response.status_code != 200


@pytest.mark.parametrize(
    "booking_id",
    ["invalid", "abc", "test-id"]
)
def test_update_with_invalid_booking_id_format(
    api_client, auth_token, booking_id
):

    updated_data = get_updated_booking_data()

    response = update_booking(
        api_client, booking_id, auth_token, updated_data
    )

    assert response.status_code != 200


# ============================================================
# 5. Invalid / Boundary Update Data
# ============================================================

def test_update_with_empty_body(api_client, auth_token):

    booking_id = create_booking(api_client)

    response = api_client.put(
        f"/booking/{booking_id}",
        json={},
        headers={"Cookie": f"token={auth_token}"}
    )

    assert response.status_code in [200, 400]


def test_update_missing_firstname(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()
    updated_data.pop("firstname")

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code in [200, 400]


def test_update_missing_lastname(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()
    updated_data.pop("lastname")

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code in [200, 400]


def test_update_missing_totalprice(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()
    updated_data.pop("totalprice")

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code in [200, 400]


def test_update_missing_depositpaid(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()
    updated_data.pop("depositpaid")

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code in [200, 400]


def test_update_missing_bookingdates(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()
    updated_data.pop("bookingdates")

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code in [200, 400]


@pytest.mark.parametrize(
    "totalprice",
    ["500", "invalid", None, [], {}]
)
def test_update_invalid_totalprice_type(
    api_client, auth_token, totalprice
):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()
    updated_data["totalprice"] = totalprice

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code in [200, 400]


@pytest.mark.parametrize(
    "depositpaid",
    ["true", "false", 1, 0, None, []]
)
def test_update_invalid_depositpaid_type(
    api_client, auth_token, depositpaid
):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()
    updated_data["depositpaid"] = depositpaid

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code in [200, 400]


def test_update_malformed_booking_dates(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    updated_data["bookingdates"] = {
        "checkin": "invalid-date",
        "checkout": "invalid-date"
    }

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code in [200, 400]


# ============================================================
# 6. Data Integrity / Lifecycle
# ============================================================

def test_create_update_get_booking(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    update_response = update_booking(
        api_client, booking_id, auth_token, updated_data
    )

    assert update_response.status_code == 200

    get_response = api_client.get(f"/booking/{booking_id}")

    assert get_response.status_code == 200
    assert get_response.json() == updated_data


def test_updated_booking_is_consistent_across_multiple_gets(
    api_client, auth_token
):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    update_response = update_booking(
        api_client, booking_id, auth_token, updated_data
    )

    assert update_response.status_code == 200

    first_get = api_client.get(f"/booking/{booking_id}")
    second_get = api_client.get(f"/booking/{booking_id}")

    assert first_get.status_code == 200
    assert second_get.status_code == 200
    assert first_get.json() == second_get.json()


def test_update_then_delete_then_get(api_client, auth_token):

    booking_id = create_booking(api_client)
    updated_data = get_updated_booking_data()

    update_response = update_booking(
        api_client, booking_id, auth_token, updated_data
    )

    assert update_response.status_code == 200

    delete_response = api_client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )

    assert delete_response.status_code == 201

    get_response = api_client.get(f"/booking/{booking_id}")

    assert get_response.status_code == 404


def test_update_preserves_supplied_unchanged_fields(api_client, auth_token):

    booking_id = create_booking(api_client)

    updated_data = get_booking_data()
    updated_data["firstname"] = "OnlyFirstnameChanged"

    response = update_booking(api_client, booking_id, auth_token, updated_data)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["firstname"] == "OnlyFirstnameChanged"
    assert response_data["lastname"] == updated_data["lastname"]
    assert response_data["totalprice"] == updated_data["totalprice"]
    assert response_data["depositpaid"] == updated_data["depositpaid"]
    assert response_data["bookingdates"] == updated_data["bookingdates"]
    assert response_data["additionalneeds"] == updated_data["additionalneeds"]