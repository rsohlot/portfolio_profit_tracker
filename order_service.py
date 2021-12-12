import json
import glob
import sys
import pandas as pd
from utility import get_data_path, format_date
from order import Order


class OrderService:
    @classmethod
    def load_orders(cls):
        path = get_data_path()
        all_files = glob.glob(path + "/*.csv")
        if len(all_files) == 0:
            print("No Files Found!!! please add files in (data/reports) to continue...")
            sys.exit(0)
        data =  pd.concat(map(pd.read_csv, all_files)) 
        data_json = json.loads(data.to_json(orient = 'records'))
        order_list = []
        for each_stock in data_json:
            trade_date = format_date(each_stock['trade_date'])
            order = Order(each_stock['symbol'],each_stock['series'],each_stock['quantity'], each_stock['price'], each_stock['trade_type'], trade_date)
            order_list.append(order)
        return order_list

    """
    save order.
    input: order object
    """
    def save_order(self, order):
        pass
    
    """
    get list of orders by trade_type
    """
    def get_orders(self):
        pass
    
    """
    get list of orders by symbol
    """
    def get_orders_by_symbol(self, symbol):
        pass
    
    """
    get list of orders by trade_date
    """
    def get_orders_by_date(self, series):
        pass

    """
    get list of orders by series
    """
    def get_orders_by_series(self, series):
        pass