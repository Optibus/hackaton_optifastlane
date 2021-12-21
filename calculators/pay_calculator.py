from calculators.calculator import Calculator
from models.option_result import OptionResult
from models.user_input import UserInput
from models.user_input_by_address import UserInputByAddress
from operators.prediction_model_operator import PredictionModelOperator
from utils.constants import FAST_LANE_START_LON, FAST_LANE_START_LAT, FAST_LANE_END_LON, FAST_LANE_END_LAT, \
    FAST_LANE_CONST_TIME, COST_PER_MINUTES_BY_CAR, PARKING_COST, FAST_LANE_START_ADDRESS, FAST_LANE_END_ADDRESS


class PayCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.prediction_model_operator = PredictionModelOperator()

    def _calculate_by_address(self, start_time: float, source_address: str, target_address: str):
        source_to_fastlane_time = self.gmaps_operator.calculate_trip_by_address(source_address, FAST_LANE_START_ADDRESS)

        fastlane_to_target_time = self.gmaps_operator.calculate_trip_by_address(FAST_LANE_END_ADDRESS, target_address)

        fastlane_time = self.gmaps_operator.calculate_trip(FAST_LANE_START_LON, FAST_LANE_START_LAT,
                                                           FAST_LANE_END_LON, FAST_LANE_END_LAT, avoid_tolls=False)

        fastlane_cost = self.prediction_model_operator.get_cost(start_time, fastlane_time)

        total_time = fastlane_time + source_to_fastlane_time + fastlane_to_target_time

        total_cost = total_time * COST_PER_MINUTES_BY_CAR + fastlane_cost + PARKING_COST
        return OptionResult(start_time, start_time + total_time, total_cost)
