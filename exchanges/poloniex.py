from exchange import Exchange


class Poloniex(Exchange):
    def __init__(self):
        super(Poloniex, self).__init__("Poloniex")

    def connect_to_api(self, api_keys):
        super(Poloniex, self).connect_to_api(api_keys)
        pass

    def get_general_coin_info(self, coin):
        pass

    def buy(self, coin, quantity, price):
        pass

    def sell(self, coin, quantity, price):
        pass

    def get_order_history(self, coin):
        pass
