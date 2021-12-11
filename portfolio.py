from stock_service import StockService
from order import OrderService

class Portfolio:
    def __init__(self, portfolio_name, order_list = None) -> None:
        self.portfolio_name = portfolio_name
        self.order_list = order_list

    def load(self, source='zerodha'):
        self.order_list = OrderService.load_orders()
        StockService.create_stock_from_orders(self.order_list)

        


    

    