import yfinance as yf
import pandas as pd
from datetime import date
import glob
import json

class DayPrice:
    def __init__(self) -> None:
        self.date = None
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        

class Stock:
    def __init__(self, stock_code:str,quantity:int,date_purchased:date, stock_name = None) -> None:
        self.stock_code  = stock_code
        self.quantity = quantity
        self.date_purchased = date_purchased
        # list of Day price
        self.stock_price:list = []

    def fetch_stock_historical_price(self):
        self.stock_price = yf.downlaod(self.stock_code)


class Portfolio:
    def __init__(self, portfolio_name, stock_list = None) -> None:
        self.portfolio_name = portfolio_name
        self.stock_list = stock_list
    
    def add_stock(self, stock: Stock):
        self.stock_list.append(stock)

    def load(self, source='zerodha', path = 'data/reports/'):
        """
        Load all the csv in the folder data/reports
        """
        data =  pd.concat(map(pd.read_csv, glob.glob(path + "/*.csv"))) 
        data_json = json.loads(data.to_json(orient = 'records'))
        for each_stock in data_json:
            stock = Stock(each_stock['symbol'],each_stock['quantity'],each_stock['trade_date'],each_stock['symbol'])
            self.stock_list.append(stock)
        # create portfolio objects from the data

    

    