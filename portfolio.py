from pandas.core import series
import yfinance as yf
import pandas as pd
from datetime import date
import glob
import json
from fetch_stock_price import fetch_stock_price
from stock_service import StockService
from utility import get_current_date
import uuid
from order import OrderService

class Portfolio:
    def __init__(self, portfolio_name, order_list = None) -> None:
        self.portfolio_name = portfolio_name
        self.order_list = order_list

    def load(self, source='zerodha'):
        self.order_list = OrderService.load_orders()
        StockService.create_stock_from_orders(self.order_list)

        


    

    