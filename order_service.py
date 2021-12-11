import uuid
import json
import glob
import pandas as pd
from utility import get_data_path
from order import Order

class OrderService:
    @staticmethod
    def load_orders(self):
        path = get_data_path()
        data =  pd.concat(map(pd.read_csv, glob.glob(path + "/*.csv"))) 
        data_json = json.loads(data.to_json(orient = 'records'))
        order_list = []
        for each_stock in data_json:
            order = Order(each_stock['symbol'],each_stock['series'],each_stock['quantity'], each_stock['price'], each_stock['trade_type'], each_stock['trade_date'])
            order_list.append(order)
        return order_list

    def save_order(self, order):
        pass

    def get_orders(self):
        pass

    def get_orders_by_symbol(self, symbol):
        pass

    def get_orders_by_series(self, series):
        pass