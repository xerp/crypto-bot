import unittest
from exchanges import loader
from exchange import EXCHANGE_COMMANDS


class ExchangeTestCase(unittest.TestCase):
    def test_get_available_exchanges(self):
        expected_length = 1

        exchanges = loader.get_available_exchanges()

        self.assertEqual(len(exchanges), expected_length, 'Available exchanges do not match')

    def test_get_exchange_by_name(self):
        name = 'Poloniex'

        exchange = loader.get_exchange_by_name(name)

        self.assertEqual(exchange.name, name, 'Exchange has not found')

    def test_command_name_decorator(self):
        expected_command_length = 4
        commands = EXCHANGE_COMMANDS

        self.assertEqual(len(commands.keys()), expected_command_length,'Commands do not match')


if __name__ == '__main__':
    unittest.main()
