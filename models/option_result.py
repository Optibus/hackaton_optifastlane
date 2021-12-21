
class OptionResult(dict):
    def __init__(self, start_time: float, end_time: float, cost: float):
        dict.__init__(self, start_time=start_time, end_time=end_time, cost=cost)
