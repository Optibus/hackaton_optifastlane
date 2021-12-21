from calculators.calculator import Calculator
from models.option_result import OptionResult
from models.user_input import UserInput
from utils.constants import FAST_LANE_START_LON, FAST_LANE_START_LAT, FAST_LANE_END_LON, FAST_LANE_END_LAT, \
    PARKING_TIME, COST_PER_MINUTES_BY_CAR, FAST_LANE_START_ADDRESS, FAST_LANE_END_ADDRESS
from utils.constants import FAST_LANE_START_LON, FAST_LANE_START_LAT, FAST_LANE_START_ADDRESS


class ParkCalculator(Calculator):
    def _calculate_by_address(self, start_time: float, source_address: str, target_address: str):
        source_to_fastlane_time = self.gmaps_operator.calculate_trip_by_address(source_address, FAST_LANE_START_ADDRESS)

        fastline_time = self.gmaps_operator.calculate_trip_by_address(FAST_LANE_START_ADDRESS,
                                                           FAST_LANE_END_ADDRESS, avoid_tolls=False)

        fastlane_to_target_time = self.gmaps_operator.calculate_trip_by_address(FAST_LANE_END_ADDRESS, target_address)

        after_parking_time = fastline_time + fastlane_to_target_time + PARKING_TIME

        total_cost = source_to_fastlane_time * COST_PER_MINUTES_BY_CAR + after_parking_time
        return OptionResult(start_time, start_time + source_to_fastlane_time + after_parking_time, total_cost)
