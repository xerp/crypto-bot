from exchange import Exchange, http_get


class Poloniex(Exchange):
    def __init__(self):
        super(Poloniex, self).__init__("Poloniex")
        self.__api_url = 'https://poloniex.com/public'
        self.__command_url = f'{self.__api_url}?command='

    def connect_to_api(self, api_keys):
        super(Poloniex, self).connect_to_api(api_keys)
        pass

    def get_general_coin_info(self, coins):
        url = f'{self.__command_url}returnTicker'
        ticker = '_'.join(coins).upper()

        try:

            response = http_get(url)
            return response[ticker]
        except KeyError:
            return {}

    def buy(self, coin, quantity, price):
        pass

    def sell(self, coin, quantity, price):
        pass

    def get_order_history(self, coin):
        pass
