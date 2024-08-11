import json
from datetime import datetime, timedelta

import pytest
import requests

from models.booking_model import Booking

BASE_BOOKING_URL: str = 'https://restful-booker.herokuapp.com/booking'
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}


@pytest.fixture(scope='session')
def auth_token():
    url = 'https://restful-booker.herokuapp.com/auth'
    payload = {
        "username": "admin",
        "password": "password123"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json().get('token')
    else:
        raise Exception(f"Failed to get auth token. Status code: {response.status_code}, Response: {response.text}")


def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def create_booking(booking_payload: dict):
    response = requests.post(BASE_BOOKING_URL, headers=HEADERS,
                             data=json.dumps(booking_payload, default=datetime_serializer))

    assert response.status_code == 200, f"Failed to create booking: {response.status_code} - {response.text}"

    new_booking = response.json()
    return new_booking


def get_booking_by_id(new_booking_id):
    response = requests.get(BASE_BOOKING_URL + '/' + str(new_booking_id), headers=HEADERS)

    assert response.status_code == 200, f"Failed to get booking: {response.status_code} - {response.text}"

    return response.json()


def update_booking(booking: Booking, token):
    HEADERS['Cookie'] = f'token= {token}'
    response = requests.put(BASE_BOOKING_URL + '/' + str(booking['bookingid']), headers=HEADERS,
                            data=json.dumps(booking['booking'], default=datetime_serializer))

    assert response.status_code == 200, f"Failed to update booking: {response.status_code} - {response.text}"

    return response.json()


#When a user creates a new booking via API then the booking appears in all booking results.
def test_new_booking_in_all_bookings():
    checkin_date = datetime.now() + timedelta(days=7)
    checkout_date = checkin_date + timedelta(days=2)

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

    new_booking_id = create_booking(booking_payload)['bookingid']
    assert get_booking_by_id(
        new_booking_id=new_booking_id), f"The new booking id {new_booking_id} does not appear in the booking results."


#When a user updates an existing booking - the booking updated successfully.
def test_update_booking(auth_token):
    checkin_date = datetime.now() + timedelta(days=7)
    checkout_date = checkin_date + timedelta(days=4)
    booking_dict = {
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

    org_booking = create_booking(booking_dict)

    org_booking['booking']['bookingdates']['checkout'] = (
            datetime.strptime(org_booking['booking']['bookingdates']['checkin'], '%Y-%m-%d') + timedelta(
        days=5)).strftime('%Y-%m-%d')

    update_booking(org_booking, auth_token)

    updated_booking = get_booking_by_id(new_booking_id=org_booking['bookingid'])

    org_booking_obj = Booking(
        firstname=org_booking.get('booking').get('firstname'),
        lastname=org_booking.get('booking').get('lastname'),
        totalprice=str(org_booking.get('booking').get('totalprice')),  # Converting to string as per the dataclass
        depositpaid=str(org_booking.get('booking').get('depositpaid')),  # Converting to string as per the dataclass
        bookingdates_checking=org_booking.get('booking').get('bookingdates').get('checkin'),
        bookingdates_checkout=org_booking.get('booking').get('bookingdates').get('checkout'),
        additionalneeds=org_booking.get('booking').get('additionalneeds')
    )

    # Create a Booking object using the JSON data
    updated_booking_obj = Booking(
        firstname=updated_booking.get('firstname'),
        lastname=updated_booking.get('lastname'),
        totalprice=str(updated_booking.get('totalprice')),  # Converting to string as per the dataclass
        depositpaid=str(updated_booking.get('depositpaid')),  # Converting to string as per the dataclass
        bookingdates_checking=updated_booking.get('bookingdates').get('checkin'),
        bookingdates_checkout=updated_booking.get('bookingdates').get('checkout'),
        additionalneeds=updated_booking.get('additionalneeds')
    )
    assert org_booking_obj.compare(updated_booking_obj), \
        f"The new booking was not updated successfully: was {updated_booking},but should have been {org_booking['booking']}"