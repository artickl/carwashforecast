#!/usr/bin/env python3

import argparse
from geopy.geocoders import Nominatim #pip install Nominatim geopy
from geopy.exc import GeocoderTimedOut

def give_me_coordinates(address):
    try:
        geolocator = Nominatim(user_agent='coordinates.py')
        location = geolocator.geocode(address, timeout=10)
        return (location.latitude, location.longitude)
    except AttributeError:
        raise ValueError('Problem with address. Cannot Geocode.')
    except GeocoderTimedOut:
        raise TimeoutError('Timeout for location request.')

def give_me_details(address):
    try:
        geolocator = Nominatim(user_agent='coordinates.py')
        location = geolocator.geocode(address, timeout=10)
        return (location.address)
    except AttributeError:
        raise ValueError('Problem with address. Cannot Geocode.')
    except GeocoderTimedOut:
        raise TimeoutError('Timeout for location request.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Geocoding addresses to coordinates:')
    parser.add_argument('-a','--address', help='Provide your location, like full address, or city with region', required=True)
    args = parser.parse_args()

    try:
        print("Details:",give_me_details(args.address))
        print("Coordinates:",give_me_coordinates(args.address))
    except Exception as e:
        print(e)
