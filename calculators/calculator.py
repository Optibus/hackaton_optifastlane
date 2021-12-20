from models.user_input import UserInput
from operators.gmaps_operator import GoogleMapsOperator
from operators.waze_operator import WazeOperator


class Calculator(object):
    def __init__(self):
        self.waze_operator = WazeOperator()
        self.gmaps_operator = GoogleMapsOperator()

    def calculate(self, user_input: UserInput):
        pass