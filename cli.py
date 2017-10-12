import sys
from exchange import EXCHANGE_COMMANDS, ExchangeNotFoundError
from exchanges import loader

CLI_COMMANDS = EXCHANGE_COMMANDS
CLI_COMMANDS['exchanges'] = loader.get_available_exchanges_by_name


def parse_option(args):
    try:
        return args[1]
    except KeyError:
        pass


if __name__ == '__main__':

    option = parse_option(sys.argv)
    function = None
    try:
        function = CLI_COMMANDS[option]
    except KeyError:
        print('Option is not valid')
        exit()

    if option == 'exchanges':
        exchanges = function()
        print(','.join(exchanges))
    else:
        try:
            exchange = loader.get_exchange_by_name(sys.argv[1])
            if not exchange:
                raise ExchangeNotFoundError(f'{exchange} exchange is not available')

            coin = sys.argv[2]

            if option == 'info':
                coin_info = function(coin)

                for k, v in coin_info.iteritems():
                    print(f'{k}::{v}')

        except IndexError:
            print('Missing arguments for this option')
            exit()
        except ExchangeNotFoundError as error:
            print(error)
            exit()
