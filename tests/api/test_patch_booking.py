import pytest

from tests.test_data.booking_data import get_booking_data
from utils.booking_helper import create_booking, patch_booking


# ============================================================
# Helper Functions
# ============================================================

def get_patch_data():
    return {
        "firstname": "PatchedMandar",
        "lastname": "PatchedBhoir",
        "totalprice": 750,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-10"
        },
        "additionalneeds": "Dinner"
    }


# ============================================================
# 1. Positive Scenarios
# ============================================================

def test_patch_existing_booking(api_client, auth_token):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "PatchedMandar"}
    )

    assert response.status_code == 200
    assert response.json()["firstname"] == "PatchedMandar"


@pytest.mark.parametrize(
    "field,value",
    [
        ("firstname", "PatchedFirst"),
        ("lastname", "PatchedLast"),
        ("totalprice", 750),
        ("depositpaid", False),
        ("additionalneeds", "Dinner"),
    ]
)
def test_patch_single_booking_field(api_client, auth_token, field, value):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token, {field: value}
    )

    assert response.status_code == 200
    assert response.json()[field] == value


def test_patch_booking_dates(api_client, auth_token):

    booking_id = create_booking(api_client)

    updated_dates = {
        "checkin": "2027-01-01",
        "checkout": "2027-01-10"
    }

    response = patch_booking(
        api_client, booking_id, auth_token,
        {"bookingdates": updated_dates}
    )

    assert response.status_code == 200
    assert response.json()["bookingdates"] == updated_dates


def test_patch_multiple_booking_fields(api_client, auth_token):

    booking_id = create_booking(api_client)

    patch_data = {
        "firstname": "MultiplePatch",
        "totalprice": 900,
        "depositpaid": False
    }

    response = patch_booking(
        api_client, booking_id, auth_token, patch_data
    )

    assert response.status_code == 200

    for field, value in patch_data.items():
        assert response.json()[field] == value


def test_patch_all_booking_fields(api_client, auth_token):

    booking_id = create_booking(api_client)
    patch_data = get_patch_data()

    response = patch_booking(
        api_client, booking_id, auth_token, patch_data
    )

    assert response.status_code == 200

    for field, value in patch_data.items():
        assert response.json()[field] == value


def test_patch_empty_object(api_client, auth_token):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token, {}
    )

    assert response.status_code in [200, 400]


# ============================================================
# 2. Partial Update / Preservation
# ============================================================

@pytest.mark.parametrize(
    "field,value",
    [
        ("firstname", "OnlyFirstChanged"),
        ("lastname", "OnlyLastChanged"),
        ("totalprice", 850),
        ("depositpaid", False),
        ("additionalneeds", "Brunch"),
    ]
)
def test_patch_preserves_other_fields(api_client, auth_token, field, value):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = patch_booking(
        api_client, booking_id, auth_token, {field: value}
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data[field] == value

    for other_field, original_value in booking_data.items():
        if other_field != field:
            assert response_data[other_field] == original_value


def test_patch_one_field_preserves_booking_dates(api_client, auth_token):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "DatePreservation"}
    )

    assert response.status_code == 200
    assert response.json()["bookingdates"] == booking_data["bookingdates"]


def test_patch_booking_twice(api_client, auth_token):

    booking_id = create_booking(api_client)

    first_response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "FirstPatch"}
    )

    second_response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "SecondPatch"}
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["firstname"] == "SecondPatch"


# ============================================================
# 3. Response Validation
# ============================================================

def test_patch_response_is_json_object(api_client, auth_token):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "ResponseCheck"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_patch_response_contains_expected_fields(api_client, auth_token):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "FieldsCheck"}
    )

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


def test_patch_response_field_types(api_client, auth_token):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "TypesCheck"}
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["firstname"], str)
    assert isinstance(data["lastname"], str)
    assert isinstance(data["totalprice"], int)
    assert isinstance(data["depositpaid"], bool)
    assert isinstance(data["bookingdates"], dict)
    assert isinstance(data["additionalneeds"], str)


def test_patch_get_booking_returns_updated_data(api_client, auth_token):

    booking_id = create_booking(api_client)

    patch_data = {"firstname": "GetAfterPatch"}

    patch_response = patch_booking(
        api_client, booking_id, auth_token, patch_data
    )

    assert patch_response.status_code == 200

    get_response = api_client.get(f"/booking/{booking_id}")

    assert get_response.status_code == 200
    assert get_response.json()["firstname"] == patch_data["firstname"]


# ============================================================
# 4. Authentication Scenarios
# ============================================================

def test_patch_without_authentication(api_client):

    booking_id = create_booking(api_client)

    response = api_client.patch(
        f"/booking/{booking_id}",
        json={"firstname": "NoAuth"}
    )

    assert response.status_code in [401, 403]


def test_patch_with_invalid_token(api_client):

    booking_id = create_booking(api_client)

    response = api_client.patch(
        f"/booking/{booking_id}",
        json={"firstname": "InvalidToken"},
        headers={"Cookie": "token=invalid-token"}
    )

    assert response.status_code in [401, 403]


def test_patch_with_malformed_token(api_client):

    booking_id = create_booking(api_client)

    response = api_client.patch(
        f"/booking/{booking_id}",
        json={"firstname": "MalformedToken"},
        headers={"Cookie": "invalid-token"}
    )

    assert response.status_code in [401, 403]


# ============================================================
# 5. Invalid Booking IDs
# ============================================================

@pytest.mark.parametrize(
    "booking_id",
    [999999999, 0, -1, -999]
)
def test_patch_invalid_numeric_booking_id(api_client, auth_token, booking_id):

    response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "InvalidID"}
    )

    assert response.status_code != 200


@pytest.mark.parametrize(
    "booking_id",
    ["invalid", "abc", "test-id"]
)
def test_patch_invalid_booking_id_format(api_client, auth_token, booking_id):

    response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "InvalidID"}
    )

    assert response.status_code != 200


# ============================================================
# 6. Invalid / Boundary Data
# ============================================================

@pytest.mark.parametrize(
    "field,value",
    [
        ("firstname", ""),
        ("lastname", ""),
        ("totalprice", "invalid"),
        ("totalprice", None),
        ("depositpaid", "invalid"),
        ("bookingdates", {}),
    ]
)
def test_patch_invalid_or_boundary_data(api_client, auth_token, field, value):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token, {field: value}
    )

    assert response.status_code in [200, 400]


@pytest.mark.parametrize(
    "field,value",
    [
        ("totalprice", "500"),
        ("totalprice", "invalid"),
        ("totalprice", None),
        ("totalprice", []),
        ("totalprice", {}),
    ]
)
def test_patch_invalid_totalprice_type(api_client, auth_token, field, value):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token, {field: value}
    )

    assert response.status_code in [200, 400]


@pytest.mark.parametrize(
    "value",
    ["true", "false", 1, 0, None, []]
)
def test_patch_invalid_depositpaid_type(api_client, auth_token, value):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token,
        {"depositpaid": value}
    )

    assert response.status_code in [200, 400]


def test_patch_malformed_booking_dates(api_client, auth_token):

    booking_id = create_booking(api_client)

    response = patch_booking(
        api_client, booking_id, auth_token,
        {
            "bookingdates": {
                "checkin": "invalid-date",
                "checkout": "invalid-date"
            }
        }
    )

    assert response.status_code in [200, 400]


# ============================================================
# 7. Data Integrity / Lifecycle
# ============================================================

def test_create_patch_get_booking(api_client, auth_token):

    booking_data = get_booking_data()
    booking_id = create_booking(api_client, booking_data)

    patch_data = {"firstname": "LifecyclePatch"}

    patch_response = patch_booking(
        api_client, booking_id, auth_token, patch_data
    )

    assert patch_response.status_code == 200

    get_response = api_client.get(f"/booking/{booking_id}")

    assert get_response.status_code == 200

    response_data = get_response.json()

    assert response_data["firstname"] == patch_data["firstname"]
    assert response_data["lastname"] == booking_data["lastname"]
    assert response_data["bookingdates"] == booking_data["bookingdates"]


def test_patch_then_delete_then_get(api_client, auth_token):

    booking_id = create_booking(api_client)

    patch_response = patch_booking(
        api_client, booking_id, auth_token,
        {"firstname": "DeleteAfterPatch"}
    )

    assert patch_response.status_code == 200

    delete_response = api_client.delete(
        f"/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"}
    )

    assert delete_response.status_code == 201

    get_response = api_client.get(f"/booking/{booking_id}")

    assert get_response.status_code == 404


def test_patch_same_booking_multiple_fields(api_client, auth_token):

    booking_id = create_booking(api_client)

    first_patch = {"firstname": "FirstNamePatch"}
    second_patch = {"lastname": "SecondLastPatch"}

    first_response = patch_booking(
        api_client, booking_id, auth_token, first_patch
    )

    second_response = patch_booking(
        api_client, booking_id, auth_token, second_patch
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    response_data = second_response.json()

    assert response_data["firstname"] == first_patch["firstname"]
    assert response_data["lastname"] == second_patch["lastname"]
