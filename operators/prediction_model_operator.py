import pandas as pd
from datetime import datetime, timedelta

from resources.last_prices import LAST_PRICES
from utils.constants import FAST_LANE_DEFAULT_PRICE

price_0 = -3.55  # -3.550434103027726
drive_time_coef = 2.28  # 2.2815069806518506
last_price_60_coef = 0.06  # 0.05924936537076222
last_price_75_coef = -0.43  # -0.43042764813524875

FIX_START = 26


class PredictionModelOperator(object):
    def __init__(self):
        self.prices_df = pd.read_csv('resources/prices.txt',
                                     names=['date_time', 'drive_time', 'xx', 'price'])
        self.prices_df['dow'] = pd.to_datetime(self.prices_df.date_time).dt.dayofweek
        self.prices_df['time'] = pd.to_datetime(self.prices_df.date_time)
        self.prices_df['day'] = self.prices_df.time.dt.date
        self.prices_df['tod'] = pd.to_datetime(self.prices_df.date_time).dt.hour * 60 + pd.to_datetime(
            self.prices_df.date_time).dt.minute

    @staticmethod
    def price_prediction(drive_time, last_price_60, last_price_75):
        if drive_time < 8:
            return 7.0
        if drive_time >= FIX_START:
            return 56 + (drive_time - 28) * 2
        return price_0 + drive_time_coef * drive_time + last_price_60_coef * last_price_60 + \
               last_price_75_coef * last_price_75

    def last_price(self, cur_time, cur_date, delta):
        if delta < 5.0:
            tmp = self.prices_df[(self.prices_df.tod == cur_time) & (self.prices_df.day == cur_date)]
        else:
            tmp = self.prices_df[(self.prices_df.tod <= cur_time - delta) & (self.prices_df.day == cur_date)]
        if not len(tmp):
            if len(self.prices_df[self.prices_df.day == cur_date]) > 0:
                return self.last_price(cur_time, cur_date, delta - 5)
            tmp = self.prices_df[(self.prices_df.tod <= cur_time - delta) & (self.prices_df.dow == cur_date.weekday())]
            if not len(tmp):
                tmp = [v for k, v in LAST_PRICES.items() if k <= cur_time - delta]
                if not len(tmp):
                    return FAST_LANE_DEFAULT_PRICE
        return tmp.price.iloc[-1]

    def get_cost(self, start_time, drive_time):
        cur_time = start_time
        cur_date = datetime.today().date()
        delta = 60
        if cur_time - delta < 0:
            cur_time = 60 * 24 - cur_time
            cur_date = datetime.today() - timedelta(days=1)
        last_price_60 = self.last_price(cur_time, cur_date, delta=delta)
        delta = 75
        if cur_time - delta < 0:
            cur_time = 60 * 24 - cur_time
            cur_date = datetime.today() - timedelta(days=1)
        last_price_75 = self.last_price(cur_time, cur_date, delta=delta)
        return self.price_prediction(drive_time, last_price_60, last_price_75)


if __name__ == '__main__':
    pred_model = PredictionModelOperator()
    res = pred_model.get_cost(8 * 60, 30)
    print(res)
