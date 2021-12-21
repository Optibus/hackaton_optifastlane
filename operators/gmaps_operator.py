import logging
import os

from datetime import datetime, timedelta
import googlemaps

api_key_env_var = 'GMAPS_API_KEY'

class GoogleMapsOperator:
    def __init__(self):
        if not api_key_env_var in os.environ:
            raise Exception("missing google maps api key in env var " + api_key_env_var)
        key = os.environ.get(api_key_env_var)
        self.gmaps = googlemaps.Client(key=key)

    def calculate_trip(self, origin_long, origin_lat, destination_long, destination_lat, minutes_from_now=0,
                       avoid_tolls=True):
        origin = self.geo_to_address_format(origin_long, origin_lat)
        target = self.geo_to_address_format(destination_long, destination_lat)
        self.calculate_trip_by_address(origin, target, minutes_from_now, avoid_tolls)


    def calculate_trip_by_address(self, origin: str, destination: str, minutes_from_now=0,
                                  avoid_tolls=True):
        arrival_time = datetime.now() + timedelta(minutes=minutes_from_now)
        directions = self.gmaps.directions(origin, destination,
                                           mode="driving",
                                           arrival_time=arrival_time,
                                           avoid="tolls" if avoid_tolls else None)
        logging.debug("response from google maps: {}".format(directions))
        return directions[0]["legs"][0]["duration"]["value"] / 60.0

    def geo_to_address_format(self, lon: float, lat: float):
        return "{},{}".format(lat, lon)

