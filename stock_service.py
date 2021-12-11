import requests
from nsepython import equity_history, nsefetch
import pandas as pd
from utility import get_current_date
from stock import Stock


class StockService:
    def equity_history(self, symbol,series,start_date,end_date):
        payload = nsefetch("https://www.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22"+series+"%22]&from="+start_date+"&to="+end_date+"")
        # return pd.DataFrame.from_records(payload["data"])
        return payload['data']


    def fetch_stock_price(self, symbol,series,start_date, end_date):
        return equity_history(symbol,series,start_date,end_date)

    @staticmethod
    def create_stock_from_orders(self, orders):
        for each_order in orders:
            # create stock object for each order
            start_date = each_order.date_purchased
            end_date  = get_current_date()
            stock = Stock(each_order['symbol'], each_order['quantity'], start_date, end_date)
            stock_price = self.fetch_stock_price(each_order.symbol,each_order.series,start_date, end_date)
            stock_price = pd.DataFrame.from_records(stock_price)
            stock.set_stock_price(stock_price)
            

