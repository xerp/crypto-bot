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

    @unittest.skip("testing skipping")
    def test_get_coin_info(self):
        coins = ['btc', 'eth']

        info = self.poloniex.get_general_coin_info(coins)

        self.assertTrue(info, 'coin info failing')

    @unittest.skip("testing skipping")
    def test_get_balance(self):
        coin = None
        balances = self.poloniex.get_balance(coin)

        self.assertTrue(balances, 'coin balance failing')

    @unittest.skip("testing skipping")
    def test_get_open_orders(self):
        coins = None
        open_orders = self.poloniex.get_open_orders(coins)

        self.assertTrue(open_orders, 'open orders failing')

    @unittest.skip("testing skipping")
    def test_get_order_history(self):
        coins = ['btc', 'eth']
        order_history = self.poloniex.get_order_history(coins)

        self.assertTrue(order_history, 'order history failing')

    @unittest.skip("testing skipping")
    def test_get_trade_history(self):
        coins = ['btc', 'eth']
        start_date = '8/10/2017'

        trade_history = self.poloniex.get_trade_history(coins, start_date)

        self.assertTrue(trade_history, 'trade history failing')

    @unittest.skip("testing skipping")
    def test_get_chart_info(self):
        coins = ['btc', 'eth']
        start_date = '8/10/2017'

        chart_info = self.poloniex.get_chart_info(coins, start_date)

        self.assertTrue(chart_info, 'chart info failing')

    @unittest.skip("testing skipping")
    def test_buy(self):
        coins = ['btc', 'sc']
        quantity = 200
        price = 0.00000060

        result = self.poloniex.buy(coins, quantity, price)
        print(result['orderNumber'])

        self.assertTrue(result['orderNumber'], 'buying coins failing')

    @unittest.skip("testing skipping")
    def test_sell(self):
        coins = ['btc', 'sc']
        quantity = 199.5
        price = 0.00000060

        result = self.poloniex.sell(coins, quantity, price)
        print(result['orderNumber'])

        self.assertTrue(result['orderNumber'], 'selling coins failing')

    @unittest.skip("testing skipping")
    def test_cancel_order(self):
        order_number = 15009693432

        result = self.poloniex.cancel_order(order_number)

        self.assertTrue(result['success'], 'cancel order failing')


if __name__ == '__main__':
    unittest.main()
