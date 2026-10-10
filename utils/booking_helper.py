from tests.test_data.booking_data import get_booking_data


def create_booking(api_client, booking_data=None):
    """
    Create a booking and return the booking ID.
    """
    if booking_data is None:
        booking_data = get_booking_data()

    response = api_client.post(
        "/booking",
        json=booking_data
    )

    assert response.status_code == 200

    return response.json()["bookingid"]


def get_booking(api_client, booking_id):
    """
    Retrieve a booking by booking ID.
    """
    return api_client.get(
        f"/booking/{booking_id}"
    )


def update_booking(api_client, booking_id, auth_token, booking_data):
    """
    Update a booking using PUT.
    """
    return api_client.put(
        f"/booking/{booking_id}",
        json=booking_data,
        headers={
            "Cookie": f"token={auth_token}"
        }
    )


def patch_booking(api_client, booking_id, auth_token, booking_data):
    """
    Partially update a booking using PATCH.
    """
    return api_client.patch(
        f"/booking/{booking_id}",
        json=booking_data,
        headers={
            "Cookie": f"token={auth_token}"
        }
    )


def delete_booking(api_client, booking_id, auth_token):
    """
    Delete a booking using DELETE.
    """
    return api_client.delete(
        f"/booking/{booking_id}",
        headers={
            "Cookie": f"token={auth_token}"
        }
    )
