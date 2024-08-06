import pytest
import requests
import json
from datetime import datetime, timedelta

# Define the API endpoints
CREATE_BOOKING_URL = 'https://restful-booker.herokuapp.com/apidoc/index.html#api-Booking-CreateBooking'
GET_BOOKING_URL = 'https://restful-booker.herokuapp.com/booking/:'
GET_ALL_BOOKING_URL = 'https://restful-booker.herokuapp.com/booking'
UPDATE_BOOKING_URL = 'https://restful-booker.herokuapp.com/booking'
# Define the headers (if needed)
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}


# Fixture to create a new booking
@pytest.fixture
def create_booking():
    # Calculate dates for next week
    checkin_date = datetime.now() + timedelta(days=7)
    checkout_date = checkin_date + timedelta(days=2)

    # Create the booking payload
    booking_payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin_date,
            "checkout": checkout_date
        },
        "additionalneeds": "Breakfast"
    }

    # Make the API request to create the booking
    response = requests.post(CREATE_BOOKING_URL, headers=HEADERS, data=json.dumps(booking_payload))

    assert response.status_code == 201, f"Failed to create booking: {response.status_code} - {response.text}"

    new_booking = response.json()
    yield new_booking

    # Teardown code (if needed)
    # Example: requests.delete(f'{CREATE_BOOKING_URL}/{new_booking["id"]}', headers=HEADERS)


# Fixture to get all bookings
@pytest.fixture
def get_all_bookings():
    response = requests.get(GET_BOOKING_URL, headers=HEADERS)

    assert response.status_code == 200, f"Failed to get bookings: {response.status_code} - {response.text}"

    return response.json()


# Function to find the new booking in all bookings
def find_booking(bookings, new_booking_id):
    if next((booking for booking in bookings if booking['id'] == new_booking_id), None):
        return True
    return False


# Test to validate that a new created booking appears in all booking results
def test_new_booking_in_all_bookings(create_booking, get_all_bookings):
    new_booking_id = create_booking['id']
    all_bookings = get_all_bookings

    assert find_booking(all_bookings, new_booking_id), "The new booking does not appear in the booking results."

def test_update_booking(create_booking, ):
    new_booking_id = create_booking['id']
    all_bookings = get_all_bookings

    assert find_booking(all_bookings, new_booking_id), "The new booking does not appear in the booking results."
