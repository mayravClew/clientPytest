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


# Fixture to get all bookings
@pytest.fixture
def get_all_bookings():
    response = requests.get(BASE_BOOKING_URL + '/', headers=HEADERS)

    assert response.status_code == 200, f"Failed to get bookings: {response.status_code} - {response.text}"

    return response.json()


def get_booking_by_id(new_booking_id):
    response = requests.get(BASE_BOOKING_URL + '/' + str(new_booking_id), headers=HEADERS)

    assert response.status_code == 200, f"Failed to get booking: {response.status_code} - {response.text}"

    return response.json()


def find_booking_by_id_from_all(all_bookings, new_booking_id):
    found = next((booking for booking in all_bookings if booking['bookingid'] == new_booking_id), None)
    return found


def update_booking(booking: Booking, token):
    HEADERS['Cookie'] = f'token= {token}'
    response = requests.put(BASE_BOOKING_URL + '/' + str(booking['bookingid']), headers=HEADERS,
                            data=json.dumps(booking['booking'], default=datetime_serializer))

    assert response.status_code == 200, f"Failed to update booking: {response.status_code} - {response.text}"

    return response.json()


def test_new_booking_in_all_bookings(get_all_bookings):
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
    get_booking_by_id(new_booking_id=new_booking_id)

    all_bookings = get_all_bookings
    assert find_booking_by_id_from_all(all_bookings, new_booking_id), f"The new booking id {new_booking_id} does not appear in the booking results."


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
            datetime.strptime(org_booking['booking']['bookingdates']['checkin'], '%Y-%m-%d') + timedelta(days=5))

    update_booking(org_booking, auth_token)

    updated_booking = get_booking_by_id(new_booking_id=org_booking['bookingid'])

    assert datetime.strptime(updated_booking['bookingdates']['checkout'], '%Y-%m-%d') == org_booking['booking']['bookingdates']['checkout'], \
        (f"The new booking was not updated successfully: was {updated_booking['bookingdates']['checkout']} "
         f"but should have been {org_booking['booking']['bookingdates']['checkout']}")
