import unittest
from exchanges import loader


class PoloniexTestCast(unittest.TestCase):
    def test_get_coin_info(self):
        poloniex = loader.get_exchange_by_name('poloniex')
        info = poloniex.get_general_coin_info(['btc', 'eth'])
        print(info)
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
