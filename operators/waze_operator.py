from bs4 import BeautifulSoup
from datetime import datetime
from urllib import request
from time import sleep


class WazeOperator:
    def calculate_trip(self, origin_long, origin_lat, destination_long, destination_lat, minutes_from_now=0):
        url_template = "http://www.waze.com/il-RoutingManager/routingRequest?from=x%3A{0}+y%3A{1}+bd%3Atrue&" \
                       "to=x%3A{2}+y%3A{3}+bd%3Atrue&timeout=60000&nPaths=1&at={4}"
        url = url_template.format(origin_long, origin_lat, destination_long, destination_lat, minutes_from_now)
        req = request.Request(url)
        req.add_header('referer', 'https://www.waze.com/en/livemap')
        req.add_header('user-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                     ' Chrome/68.0.3440.106 Safari/537.36')

        attempt = 1
        while True:
            try:
                print("requesting waze in url: {}".format(url))
                response = request.urlopen(req, timeout=10).read()
                break
            except Exception as e:
                print(u"Got an error during HTTP request, attempt #{}".format(attempt))
                print(str(e))
                attempt += 1
                if attempt > 3:
                    error_message = "Could not find route from {},{} -> {},{}".format(
                        origin_long, origin_lat, destination_long, destination_lat)
                    print(error_message)
                    return -1, -1, ""
                sleep(1)
        try:
            soup = BeautifulSoup(response, 'html.parser')
            travel_time = int(soup.find('total_route_time').contents[0]) / 60
            distance = float(soup.find_all('length')[-1].contents[0]) / 1000
            return travel_time, distance, str(response)
        except Exception as e:
            print("error while parsing response from waze: {}".format(e))
            return -1, -1, ""
