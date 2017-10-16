import sys
from exchange import EXCHANGE_COMMANDS, ExchangeError
from exchanges import loader

CLI_COMMANDS = EXCHANGE_COMMANDS
CLI_COMMANDS['exchanges'] = map, lambda e: e.name, loader.get_available_exchanges

CLI_FUNCTIONS = {}


# ------------ CLI Utils Functions BEGIN ------------------

def cli_exit(message=None, exit_code=0):
    if message:
        print(message)

    exit(exit_code)


def get_cli_option(args):
    try:
        return args[1]
    except IndexError:
        cli_exit('no option to perform')


def get_cli_function(option):
    try:
        return CLI_COMMANDS[option]
    except KeyError:
        cli_exit('Option is not valid')


def print_exchange_values(**kwargs):
    for parameter, parameter_value in kwargs.items():
        print(f'{parameter}::{parameter_value}')


def print_exchange_option(option, exchange_function, args):
    try:
        exchange_name = args[1]
        exchange = loader.get_exchange_by_name(exchange_name)
        if not exchange:
            raise ExchangeError(f'{exchange_name} exchange is not available')

        exchange_args = args[2::]
        CLI_FUNCTIONS[option](exchange_function, exchange_args)

        cli_exit()

    except (IndexError, ExchangeError) as error:
        if error == ExchangeError:
            cli_exit(error)
        else:
            cli_exit('Missing arguments for this option')


# ------------ CLI Utils Functions END ------------------


# ------------ CLI Functions BEGIN ------------------

def print_exchanges(cli_function):
    try:
        exchanges = cli_function[0](cli_function[1], cli_function[3])
        print(','.join(exchanges))
    except IndexError:
        cli_exit('exchanges command value must be a tuple structured as [function,lambda expression, list]')


def process_info(exchange_function, exchange_args):
    coin = exchange_args[1]

    coin_info = exchange_function(coin)
    print_exchange_values(coin_info)


# ------------ CLI Functions END ------------------


CLI_FUNCTIONS = {
    'info': process_info
}

if __name__ == '__main__':

    cli_option = get_cli_option(sys.argv)
    cli_function = get_cli_function(cli_option)

    if cli_option == 'exchanges':
        print_exchanges(cli_function)
    else:
        print_exchange_option(cli_option, cli_function, sys.argv)
