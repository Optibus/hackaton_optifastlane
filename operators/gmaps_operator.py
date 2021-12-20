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

    def calculate_trip(self, origin_long, origin_lat, destination_long, destination_lat, minutes_from_now=0):
        origin = "{},{}".format(origin_lat, origin_long)
        target = "{},{}".format(destination_lat, destination_long)
        arrival_time = datetime.now() + timedelta(minutes=minutes_from_now)
        directions = self.gmaps.directions(origin, target,
                              mode="driving",
                              arrival_time=arrival_time)
        logging.debug("response from google maps: {}".format(directions))
        return directions[0]["legs"][0]["duration"]["value"] / 60.0


