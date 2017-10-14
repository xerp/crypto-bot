from abc import ABC, abstractmethod
import requests as http

EXCHANGE_COMMANDS = {}


def http_get(url, headers=None):
    r = http.get(url, headers=headers) if headers else http.get(url)
    return r.json()


def http_post(url, data, headers=None):
    r = http.post(url, data=data, headers=headers) if headers else  http.post(url, data)
    return r.json()


def command_name(name=None):
    def wrapper(func):
        function_name = func.__name__

        if name:
            EXCHANGE_COMMANDS[name] = function_name
        else:
            EXCHANGE_COMMANDS[function_name] = function_name
        return func

    return wrapper


class ExchangeError(Exception):
    pass


class ExchangeMethodNotImplementedError(ExchangeError):
    pass


class ExchangeNotFoundError(ExchangeError):
    pass


class Exchange(ABC):
    def __init__(self, name):
        self.name = name
        self._api_keys = {}

    def connect_to_api(self, api_keys):
        self._api_keys = api_keys

    @abstractmethod
    @command_name('info')
    def get_general_coin_info(self, coins):
        pass

    @abstractmethod
    @command_name('order_history')
    def get_order_history(self, coins, depth):
        pass

    @abstractmethod
    @command_name('trade_history')
    def get_trade_history(self, coins, start_date, end_date):
        pass

    @abstractmethod
    @command_name('chart')
    def get_chart_info(self, coins, start_date, end_date, candlestick_period):
        pass

    @abstractmethod
    @command_name('balance')
    def get_balance(self, coin):
        pass

    @abstractmethod
    @command_name('open_orders')
    def get_open_orders(self, coins):
        pass

    @abstractmethod
    @command_name()
    def buy(self, coins, quantity, price):
        pass

    @abstractmethod
    @command_name()
    def sell(self, coins, quantity, price):
        pass

    @abstractmethod
    @command_name()
    def cancel_order(self, order_number):
        pass
