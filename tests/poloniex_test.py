import unittest
from exchanges import loader

api_keys = {
    'key': '',
    'secret': ''
}


class PoloniexTestCast(unittest.TestCase):
    def setUp(self):
        self.poloniex = loader.get_exchange_by_name('poloniex')
        self.poloniex.connect_to_api(api_keys)

    def test_get_coin_info(self):
        coins = ['btc', 'eth']

        info = self.poloniex.get_general_coin_info(coins)

        self.assertTrue(info, 'coin info failing')

    def test_get_balance(self):
        coin = None
        balances = self.poloniex.get_balance(coin)

        self.assertTrue(balances, 'coin balance failing')

    def test_get_open_orders(self):
        coins = None
        open_orders = self.poloniex.get_open_orders(coins)

        self.assertTrue(open_orders, 'open orders failing')

    def test_get_order_history(self):
        coins = ['btc', 'eth']
        order_history = self.poloniex.get_order_history(coins)

        self.assertTrue(order_history, 'order history failing')

    def test_get_trade_history(self):
        coins = ['btc', 'eth']
        start_date = '8/10/2017'

        trade_history = self.poloniex.get_trade_history(coins, start_date)

        self.assertTrue(trade_history, 'trade history failing')

    def test_get_chart_info(self):
        coins = ['btc', 'eth']
        start_date = '8/10/2017'

        chart_info = self.poloniex.get_chart_info(coins, start_date)

        self.assertTrue(chart_info, 'chart info failing')

    def test_buy(self):
        coins = ['btc', 'eth']
        quantity = 1
        price = 0

        result = self.poloniex.buy(coins, quantity, price)

        self.assertTrue(result['success'], 'buying coins failing')

    def test_sell(self):
        coins = ['btc', 'eth']
        quantity = 1
        price = 0

        result = self.poloniex.sell(coins, quantity, price)

        self.assertTrue(result['success'], 'selling coins failing')

    def test_cancel_order(self):
        order_number = 1

        result = self.poloniex.cancel_order(order_number)

        self.assertTrue(result['success'], 'cancel order failing')


if __name__ == '__main__':
    unittest.main()
