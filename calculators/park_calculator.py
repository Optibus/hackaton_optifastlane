from calculators.calculator import Calculator
from models.user_input import UserInput
from utils.constants import FAST_LANE_START_LON, FAST_LANE_START_LAT, FAST_LANE_END_LON, FAST_LANE_END_LAT, \
    PARKING_TIME, COST_PER_MINUTES_BY_CAR


class ParkCalculator(Calculator):
    def calculate(self, user_input: UserInput):
        source_to_fastlane_time = self.gmaps_operator.calculate_trip(user_input.source_lon, user_input.source_lat,
                                                                     FAST_LANE_START_LON, FAST_LANE_START_LAT)

        fastline_time = self.gmaps_operator.calculate_trip(FAST_LANE_START_LON, FAST_LANE_START_LAT,
                                                           FAST_LANE_END_LON, FAST_LANE_END_LAT, avoid_tolls=False)

        fastlane_to_target_time = self.gmaps_operator.calculate_trip(FAST_LANE_END_LON, FAST_LANE_END_LAT,
                                                                     user_input.target_lon, user_input.target_lat)

        after_parking_time = fastline_time + fastlane_to_target_time + PARKING_TIME

        total_cost = source_to_fastlane_time * COST_PER_MINUTES_BY_CAR + after_parking_time
        return total_cost
