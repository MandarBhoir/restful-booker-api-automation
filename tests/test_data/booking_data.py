from copy import deepcopy


BOOKING_DATA = {
    "firstname": "Mandar",
    "lastname": "Bhoir",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-10-10",
        "checkout": "2026-10-15"
    },
    "additionalneeds": "Breakfast"
}


def get_booking_data():
    """
    Return a fresh copy of the default booking data.
    """

    return deepcopy(BOOKING_DATA)