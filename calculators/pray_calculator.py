from calculators.calculator import Calculator
from models.option_result import OptionResult
from models.user_input import UserInput
from models.user_input_by_address import UserInputByAddress
from utils.constants import COST_PER_MINUTES_BY_CAR, PARKING_COST


class PrayCalculator(Calculator):
    def _calculate_by_address(self, start_time: float, source_address: str, target_address: str):
        gmaps_time = self.gmaps_operator.calculate_trip_by_address(source_address, target_address)

        cost = COST_PER_MINUTES_BY_CAR * gmaps_time + PARKING_COST
        return OptionResult(start_time, start_time + gmaps_time, cost)
