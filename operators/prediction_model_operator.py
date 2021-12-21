import pandas as pd
from datetime import datetime

price_0 = -3.55  # -3.550434103027726
drive_time_coef = 2.28  # 2.2815069806518506
last_price_60_coef = 0.06  # 0.05924936537076222
last_price_75_coef = -0.43  # -0.43042764813524875

FIX_START = 26


class PredictionModelOperator(object):
    def __init__(self):
        self.prices_df = pd.read_csv('../resources/prices.txt',
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
            tmp = self.prices_df[(self.prices_df.tod <= cur_time - delta) & (self.prices_df.dow == cur_date)]
        if not len(tmp):
            return self.last_price(cur_time, cur_date, delta - 5)
        return tmp.price.iloc[-1]

    def get_cost(self, drive_time):
        today_dow = datetime.today().weekday()
        last_price_60 = self.last_price(drive_time, today_dow, delta=60)
        last_price_75 = self.last_price(drive_time, today_dow, delta=75)
        return self.price_prediction(drive_time, last_price_60, last_price_75)


if __name__ == '__main__':
    pred_model = PredictionModelOperator()
    res = pred_model.get_cost(600)
    print(res)
