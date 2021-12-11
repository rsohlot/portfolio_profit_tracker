from datetime import date

class DayPrice:
    def __init__(self, date, open, close, high, low, last_traded_price,previous_close_price,total_traded_quantity,total_traded_value,total_trades) -> None:
        self.date = None
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.last_traded_price = None
        self.previous_close_price = None
        self.total_traded_quantity = None
        self.total_traded_value = None
        self.total_trades = None
        

class Stock:
    def __init__(self, symbol:str,series:str ,first_date:date,last_date:date ,stock_name = None) -> None:
        self.symbol  = symbol
        self.series = series
        self.first_date = first_date
        self.last_date = last_date
        self.stock_52_week_high = None
        self.stock_52_week_low = None
        self.stock_name = stock_name
        if stock_name is None:
            self.stock_name = symbol
        # list of Day price
        self.stock_price:list = []

    def set_stock_price(self,stock_price:list) -> None:
        self.stock_price = stock_price