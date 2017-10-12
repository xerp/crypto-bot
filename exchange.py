from abc import ABC, abstractmethod
import requests as http

EXCHANGE_COMMANDS = {}


def http_get(url, api_key):
    r = http.get(url)
    return r.json()


def http_post(url, data, api_key):
    r = http.post(url, data)
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


class ExchangeNotFoundError(Exception):
    pass


class Exchange(ABC):
    def __init__(self, name):
        self.name = name
        self._api_keys = {}

    @abstractmethod
    def connect_to_api(self, api_keys):
        self._api_keys = api_keys

    @abstractmethod
    @command_name('info')
    def get_general_coin_info(self, coin):
        pass

    @abstractmethod
    @command_name()
    def buy(self, coin, quantity, price):
        pass

    @abstractmethod
    @command_name()
    def sell(self, coin, quantity, price):
        pass

    @abstractmethod
    @command_name('order_history')
    def get_order_history(self, coin):
        pass
