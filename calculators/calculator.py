from models.user_input import UserInput
from models.user_input_by_address import UserInputByAddress
from operators.gmaps_operator import GoogleMapsOperator
from operators.waze_operator import WazeOperator


class Calculator(object):
    def __init__(self):
        self.waze_operator = WazeOperator()
        self.gmaps_operator = GoogleMapsOperator()

    def calculate(self, start_time: float, user_input: UserInput):
        source_address = self.gmaps_operator.geo_to_address_format(user_input.source_lon, user_input.source_lat)
        target_address = self.gmaps_operator.geo_to_address_format(user_input.target_lon, user_input.target_lat)
        return self._calculate_by_address(start_time, source_address, target_address)

    def calculate_by_address_input(self, start_time:float, user_input: UserInputByAddress):
        return self._calculate_by_address(start_time, user_input.source, user_input.target)

    def _calculate_by_address(self, start_time: float, source_address: str, target_address: str):
        pass