from calculators.calculator import Calculator
from models.option_result import OptionResult
from models.user_input import UserInput
from utils.constants import COST_PER_MINUTES_BY_CAR, PARKING_COST


class PrayCalculator(Calculator):
    def calculate(self, user_input: UserInput):
        gmaps_time = self.gmaps_operator.calculate_trip(
            user_input.source_lon, user_input.source_lat, user_input.target_lon, user_input.target_lat
        )

        cost = COST_PER_MINUTES_BY_CAR * gmaps_time + PARKING_COST
        return OptionResult(gmaps_time, cost)
