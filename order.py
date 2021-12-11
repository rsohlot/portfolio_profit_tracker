import uuid
import pandas as pd


class Order:
    def __init__(self, symbol,order_series, quantity, price, order_type, order_date):
        self.order_id = uuid.uuid4()
        self.symbol = symbol
        self.series =order_series
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.order_date = order_date

    def create_order_df(self):
        order_df = pd.DataFrame(columns=["order_id", "symbol", "series", "quantity", "price", "order_type"])
        return order_df

    def create_order(self):
        order_dict = {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "series": self.series,
            "quantity": self.quantity,
            "price": self.price,
            "order_type": self.order_type
        }   
        return order_dict

    def __str__(self):
        return "Order ID: {}, Symbol: {}, Series: {}, Quantity: {}, Price: {}, Order Type: {}".format(self.order_id, self.symbol, self.series, self.quantity, self.price, self.order_type)

    def __repr__(self):
        return "Order ID: {}, Symbol: {}, Series: {}, Quantity: {}, Price: {}, Order Type: {}".format(self.order_id, self.symbol, self.series, self.quantity, self.price, self.order_type)

    def __eq__(self, other):
        return self.order_id == other.order_id
    
    def __hash__(self):
        return hash(self.order_id)