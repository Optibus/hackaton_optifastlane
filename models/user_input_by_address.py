class UserInputByAddress(object):
    def __init__(self, source: str, target: str, latest_arrival_time: int, cost_time_slider=1.0):
        self.source = source
        self.target = target
        self.latest_arrival_time = latest_arrival_time
        self.cost_time_slider = cost_time_slider
