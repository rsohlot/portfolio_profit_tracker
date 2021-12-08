import yfinance as yf

class Stock:
    def __init__(self, stock_code:str, stock_name = None) -> None:
        self.stock_code  = stock_code
        self.stock_price = None

    def fetch_stock_historical_price(self):
        self.stock_price = yf.downlaod(self.stock_code)


class Portfolio:
    def __init__(self, portfolio_name, stock_list = None) -> None:
        self.portfolio_name = portfolio_name
        self.stock_list = stock_list
    
    def add_stock(self, stock: Stock):
        self.stock_list.append(stock)
    

    