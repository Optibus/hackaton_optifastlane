from calculators.calculator import Calculator
from models.option_result import OptionResult
from models.user_input import UserInput
from operators.prediction_model_operator import PredictionModelOperator
from utils.constants import FAST_LANE_START_LON, FAST_LANE_START_LAT, FAST_LANE_END_LON, FAST_LANE_END_LAT, \
    FAST_LANE_CONST_TIME, COST_PER_MINUTES_BY_CAR, PARKING_COST


class PayCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.prediction_model_operator = PredictionModelOperator()

    def calculate(self, start_time, user_input: UserInput):
        source_to_fastlane_time = self.gmaps_operator.calculate_trip(user_input.source_lon, user_input.source_lat,
                                                                     FAST_LANE_START_LON, FAST_LANE_START_LAT)

        fastlane_to_target_time = self.gmaps_operator.calculate_trip(FAST_LANE_END_LON, FAST_LANE_END_LAT,
                                                                     user_input.target_lon, user_input.target_lat)

        fastline_time = self.gmaps_operator.calculate_trip(FAST_LANE_START_LON, FAST_LANE_START_LAT,
                                                           FAST_LANE_END_LON, FAST_LANE_END_LAT, avoid_tolls=False)

        fastlane_cost = self.prediction_model_operator.get_cost(start_time, fastline_time)

        total_time = fastline_time + source_to_fastlane_time + fastlane_to_target_time

        total_cost = total_time * COST_PER_MINUTES_BY_CAR + fastlane_cost + PARKING_COST
        return OptionResult(start_time, start_time + total_time, total_cost)
