
class OptionResult(dict):
    def __init__(self, time: float, cost: float):
        dict.__init__(self, time=time, cost=cost)

