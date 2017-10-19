import sys
from exchange import EXCHANGE_COMMANDS, ExchangeError
from exchanges import loader
import config

CLI_FUNCTIONS = {}


# #################################################
# ------------ CLI Utils Functions BEGIN ----------
# #################################################


def cli_function(name):
    def wrapper(func):
        function_name = func.__name__

        CLI_FUNCTIONS[name] = function_name

        return func

    return wrapper


def cli_exit(message=None, exit_code=0):
    if message:
        print(message)

    exit(exit_code)


def get_cli_option(args):
    try:
        return args[1]
    except IndexError:
        cli_exit('no option to perform')


def get_exchange_function(option):
    try:
        return EXCHANGE_COMMANDS[option]
    except KeyError:
        cli_exit('Option is not valid')


def print_exchange_values(**kwargs):
    for parameter, parameter_value in kwargs.items():
        print(f'{parameter}::{parameter_value}')


def print_exchange_option(option, exchange_func, args):
    try:
        exchange_name = args[1].lower()
        exchange = loader.get_exchange_by_name(exchange_name)
        if not exchange:
            raise ExchangeError(f'{exchange_name} exchange is not available')

        exchange.connect_to_api(config.EXCHANGES[exchange_name])

        exchange_args = args[2::]
        exchange_func = getattr(exchange, exchange_func)
        CLI_FUNCTIONS[option](exchange_func, exchange_args)

        cli_exit()

    except (IndexError, ExchangeError) as error:
        if error == ExchangeError:
            cli_exit(error)
        else:
            cli_exit('Missing arguments for this option')


# #################################################
# ------------ CLI Utils Functions END ------------
# #################################################

# #################################################
# ------------ CLI Functions BEGIN ----------------
# #################################################

def print_exchanges():
    try:
        exchanges = map(lambda e: e.name, loader.get_available_exchanges())
        print(','.join(exchanges))
    except IndexError:
        cli_exit('exchanges command value must be a tuple structured as [function,lambda expression, list]')


@cli_function('info')
def process_info(exchange_func, exchange_args):
    coin = exchange_args[0]

    coin_info = exchange_func(coin)
    print_exchange_values(coin_info)


@cli_function('order_history')
def process_order_history(exchange_func, exchange_args):
    coins = [exchange_args[0], exchange_args[1]]

    history = exchange_func(coins)
    print_exchange_values(history)


@cli_function('trade_history')
def process_trade_history(exchange_func, exchange_args):
    coins = [exchange_args[0], exchange_args[1]]
    start_date = exchange_args[2]

    history = exchange_func(coins, start_date)
    print_exchange_values(history)


@cli_function('chart')
def process_chart(exchange_func, exchange_args):
    coins = [exchange_args[0], exchange_args[1]]
    start_date = exchange_args[2]

    chart = exchange_func(coins, start_date)
    print_exchange_values(chart)


@cli_function('balance')
def process_balance(exchange_func, exchange_args):
    coin = exchange_args[0]

    balance = exchange_func(coin)
    print_exchange_values(balance)


@cli_function('open_orders')
def process_open_orders(exchange_func, exchange_args):
    coins = [exchange_args[0], exchange_args[1]]

    open_orders = exchange_func(coins)
    print_exchange_values(open_orders)


@cli_function('buy')
def process_buy(exchange_func, exchange_args):
    coins = [exchange_args[0], exchange_args[1]]
    quantity = exchange_args[2]
    price = exchange_args[3]

    result = exchange_func(coins, quantity, price)
    print_exchange_values(result)


@cli_function('sell')
def process_sell(exchange_func, exchange_args):
    coins = [exchange_args[0], exchange_args[1]]
    quantity = exchange_args[2]
    price = exchange_args[3]

    result = exchange_func(coins, quantity, price)
    print_exchange_values(result)


@cli_function('cancel_order')
def process_cancel_order(exchange_func, exchange_args):
    order_number = exchange_args[0]

    result = exchange_func(order_number)
    print_exchange_values(result)


# #################################################
# ------------ CLI Functions END ------------------
# #################################################

if __name__ == '__main__':

    cli_option = get_cli_option(sys.argv)
    exchange_function = get_exchange_function(cli_option)

    if cli_option == 'exchanges':
        print_exchanges()
    else:
        print_exchange_option(cli_option, exchange_function, sys.argv)
