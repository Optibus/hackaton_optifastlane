from calculators.calculator import Calculator
from models.user_input import UserInput
from utils.constants import FAST_LANE_START_LON, FAST_LANE_START_LAT


class ParkCalculator(Calculator):
    def calculate(self, user_input: UserInput):
        source_to_fastlane_time = self.gmaps_operator.calculate_trip(user_input.source_lon, user_input.source_lat,
                                                                     FAST_LANE_START_LON, FAST_LANE_START_LAT)


        return "park"