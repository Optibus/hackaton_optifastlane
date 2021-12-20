class UserInput(object):
    def __init__(self, source_lon: float, source_lat: float, target_lon: float, target_lat: float):
        self.source_lon = source_lon
        self.source_lat = source_lat
        self.target_lon = target_lon
        self.target_lat = target_lat