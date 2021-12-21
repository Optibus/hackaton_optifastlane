class UserInput(object):
    def __init__(self, source_lon: float, source_lat: float, target_lon: float, target_lat: float,
                 latest_arrival_time: int):
        self.source_lon = source_lon
        self.source_lat = source_lat
        self.target_lon = target_lon
        self.target_lat = target_lat
        self.latest_arrival_time = latest_arrival_time
