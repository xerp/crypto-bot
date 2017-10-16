# API DOCUMENTATION: https://poloniex.com/support/api/

from urllib.parse import urlencode
from exchange import Exchange, http_get, http_post, ExchangeError, ExchangeMethodNotImplementedError
from hmac import new as hmac_new
from hashlib import sha512
import time
from datetime import datetime


def poloniex_http_post(url, data, api_keys):
    data['nonce'] = int(time.time() * 1000)
    sign = hmac_new(api_keys['secret'].encode('utf-8'),
                    urlencode(data).encode('utf-8'),
                    sha512).hexdigest()

    headers = {
        'Key': api_keys['key'],
        'Sign': sign
    }
    return http_post(url, data, headers)


def get_ticker(coins):
    return '_'.join(coins).upper()


class CandleStickPeriod:
    MINUTE_5 = 300
    MINUTE_15 = 900
    MINUTE_30 = 1800
    HOUR_2 = 7200
    HOUR_4 = 14400
    DAY_1 = 86400


class Poloniex(Exchange):
    def __init__(self):
        super(Poloniex, self).__init__("Poloniex")
        self.__public_api_url = 'https://poloniex.com/public'
        self.__trading_api_url = 'https://poloniex.com/tradingApi'

    def __trading_api_request(self, **kwargs):
        response = poloniex_http_post(self.__trading_api_url, kwargs, self._api_keys)

        if 'error' in response:
            raise ExchangeError(response['error'])

        return response

    def __public_api_request(self, **kwargs):
        parameters = urlencode(kwargs)
        url = f'{self.__public_api_url}?{parameters}'

        response = http_get(url)

        if 'error' in response:
            raise ExchangeError(response['error'])

        return response

    def get_general_coin_info(self, coins):
        ticker = get_ticker(coins)
        response = self.__public_api_request(command='returnTicker')

        try:
            return response[ticker]
        except KeyError:
            pass

    def get_order_history(self, coins, depth=10):
        ticker = get_ticker(coins)

        return self.__public_api_request(command='returnOrderBook', currencyPair=ticker, depth=depth)

    def get_trade_history(self, coins, start_date, end_date=datetime.now()):
        ticker = get_ticker(coins)
        start_time = time.mktime(datetime.strptime(start_date, "%d/%m/%Y").timetuple())
        end_time = end_date.timestamp()

        return self.__public_api_request(command='returnTradeHistory',
                                         currencyPair=ticker,
                                         start=start_time,
                                         end=end_time)

    def get_chart_info(self, coins, start_date, end_date=datetime.now(), candlestick_period=CandleStickPeriod.HOUR_4):
        ticker = get_ticker(coins)
        start_time = time.mktime(datetime.strptime(start_date, "%d/%m/%Y").timetuple())
        end_time = end_date.timestamp()

        return self.__public_api_request(command='returnChartData',
                                         currencyPair=ticker,
                                         start=start_time,
                                         end=end_time,
                                         period=candlestick_period)

    def get_balance(self, coin=None):
        all_balances = self.__trading_api_request(command='returnBalances')

        try:
            return all_balances[coin]
        except KeyError:
            return {coin: balance for (coin, balance) in all_balances.items() if float(balance) > 0}

    def buy(self, coins, quantity, price):
        ticker = get_ticker(coins)

        return self.__trading_api_request(command='buy', currencyPair=ticker, rate=price, amount=quantity)

    def sell(self, coins, quantity, price):
        ticker = get_ticker(coins)

        return self.__trading_api_request(command='sell', currencyPair=ticker, rate=price, amount=quantity)

    def cancel_order(self, order_number):
        return self.__trading_api_request(command='cancelOrder', orderNumber=order_number)

    def get_open_orders(self, coins=None):
        ticker = get_ticker(coins) if coins else 'all'

        return self.__trading_api_request(command='returnOpenOrders', currencyPair=ticker)
