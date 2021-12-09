import yfinance as yf

class DayPrice:
    def __init__(self) -> None:
        self.date = None
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        

class Stock:
    def __init__(self, stock_code:str, stock_name = None) -> None:
        self.stock_code  = stock_code
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
    

    