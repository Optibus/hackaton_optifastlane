import logging

from flask import Flask, request
from flask import jsonify

from app.error import Error
from calculators.park_calculator import ParkCalculator
from calculators.pay_calculator import PayCalculator
from calculators.pray_calculator import PrayCalculator
from models.user_input import UserInput
from models.user_input_by_address import UserInputByAddress
from operators.gmaps_operator import GoogleMapsOperator
from datetime import datetime
from operators.waze_operator import WazeOperator

app = Flask(__name__)

gmaps_operator = GoogleMapsOperator()
waze_operator = WazeOperator()
pray_calculator = PrayCalculator()
pay_calculator = PayCalculator()
park_calculator = ParkCalculator()

@app.route("/routes_options", methods=["POST"])
def routes_options():
    payload_json = request.get_json()
    user_input = UserInput(
        payload_json["source_lon"],
        payload_json["source_lat"],
        payload_json["target_lon"],
        payload_json["target_lat"],
        payload_json["latest_arrival_time"]
    )

    try:
        print("user_input={}".format(user_input))

        prev_pray_result = None
        time_now = datetime.now()
        start_time = time_now.hour * 60 + time_now.minute
        while True:
            pray_result = pray_calculator.calculate(start_time, user_input)
            if pray_result['end_time'] > user_input.latest_arrival_time:
                pray_result = prev_pray_result if prev_pray_result else pray_result
                break
            prev_pray_result = pray_result
            start_time = start_time + 5

        prev_pay_result = None
        time_now = datetime.now()
        start_time = time_now.hour * 60 + time_now.minute
        while True:
            pay_result = pay_calculator.calculate(start_time, user_input)
            if pay_result['end_time'] > user_input.latest_arrival_time:
                pay_result = prev_pay_result if prev_pay_result else pay_result
                break
            prev_pay_result = pay_result
            start_time = start_time + 5

        prev_park_result = None
        time_now = datetime.now()
        start_time = time_now.hour * 60 + time_now.minute
        while True:
            park_result = park_calculator.calculate(start_time, user_input)
            if park_result['end_time'] > user_input.latest_arrival_time:
                park_result = prev_park_result if prev_park_result else park_result
                break
            prev_park_result = park_result
            start_time = start_time + 5
        return ({
                    'pray_result': pray_result,
                    'pay_result': pay_result,
                    'park_result': park_result,
                },
                200)

    except Error as error:
        logging.exception(error)
        return jsonify(error), error.status_code
    except Exception as error:
        logging.exception(error)
        return {'message': 'Internal Server Error'}, 500


@app.route("/routes_options/by_address", methods=["POST"])
def routes_options_by_address():
    payload_json = request.get_json()
    user_input = UserInputByAddress(
        payload_json["source"],
        payload_json["target"],
        payload_json["latest_arrival_time"]
    )


    try:
        print("user_input={}".format(user_input))

        prev_pray_result = None
        time_now = datetime.now()
        start_time = time_now.hour * 60 + time_now.minute
        min_cost_result = None
        while True:
            pray_result = pray_calculator.calculate_by_address_input(start_time, user_input)
            if pray_result['end_time'] > user_input.latest_arrival_time:
                pray_result = prev_pray_result if prev_pray_result else pray_result
                if min_cost_result is not None and min_cost_result['cost'] < pray_result['cost'] \
                        and user_input.cost_time_slider <= 0.5:
                    pray_result = min_cost_result
                break
            prev_pray_result = pray_result
            if min_cost_result is None or pray_result['cost'] <= min_cost_result['cost']:
                min_cost_result = pray_result
            start_time = start_time + 5

        prev_pay_result = None
        time_now = datetime.now()
        start_time = time_now.hour * 60 + time_now.minute
        min_cost_result = None
        while True:
            pay_result = pay_calculator.calculate_by_address_input(start_time, user_input)
            if pay_result['end_time'] > user_input.latest_arrival_time:
                pay_result = prev_pay_result if prev_pay_result else pay_result
                if min_cost_result is not None and min_cost_result['cost'] < pay_result['cost'] \
                        and user_input.cost_time_slider <= 0.5:
                    pay_result = min_cost_result
                break
            prev_pay_result = pay_result
            if min_cost_result is None or pay_result['cost'] <= min_cost_result['cost']:
                min_cost_result = pay_result
            start_time = start_time + 5

        prev_park_result = None
        time_now = datetime.now()
        start_time = time_now.hour * 60 + time_now.minute
        min_cost_result = None
        while True:
            park_result = park_calculator.calculate_by_address_input(start_time, user_input)
            if park_result['end_time'] > user_input.latest_arrival_time:
                park_result = prev_park_result if prev_park_result else park_result
                if min_cost_result is not None and min_cost_result['cost'] < park_result['cost'] \
                        and user_input.cost_time_slider <= 0.5:
                    park_result = min_cost_result
                break
            prev_park_result = park_result
            if min_cost_result is None or park_result['cost'] <= min_cost_result['cost']:
                min_cost_result = park_result
            start_time = start_time + 5
        return ({
                    'pray_result': pray_result,
                    'pay_result': pay_result,
                    'park_result': park_result,
                },
                200)

    except Error as error:
        logging.exception(error)
        return jsonify(error), error.status_code
    except Exception as error:
        logging.exception(error)
        return {'message': 'Internal Server Error'}, 500

