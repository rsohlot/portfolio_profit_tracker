import uuid
from utility import get_data_path

class Order:
    def __init__(self, symbol,order_series, quantity, price, order_type, order_date):
        self.order_id = uuid.uuid4()
        self.symbol = symbol
        self.series =order_series
        self.quantity = quantity
        self.price = price
        self.order_type = order_type

