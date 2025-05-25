import unittest
import accounts
import datetime
from unittest.mock import patch

class TestAccounts(unittest.TestCase):

    def test_get_share_price(self):
        self.assertEqual(accounts.get_share_price("AAPL"), 170.00)
        self.assertEqual(accounts.get_share_price("TSLA"), 250.00)
        self.assertEqual(accounts.get_share_price("GOOGL"), 2700.00)
        self.assertEqual(accounts.get_share_price("MSFT"), 100.00)

    def test_account_initialization(self):
        account = accounts.Account("123", 1000.0)
        self.assertEqual(account.account_id, "123")
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.holdings, {})
        self.assertEqual(account.initial_deposit, 1000.0)
        self.assertEqual(len(account.transactions), 0)

    def test_deposit(self):
        account = accounts.Account("456")
        account.deposit(500.0)
        self.assertEqual(account.balance, 500.0)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0]['type'], 'deposit')
        self.assertEqual(account.transactions[0]['amount'], 500.0)

    def test_deposit_invalid_amount(self):
        account = accounts.Account("789")
        with self.assertRaises(ValueError) as context:
            account.deposit(-100.0)
        self.assertEqual(str(context.exception), "Deposit amount must be positive.")

    def test_withdraw(self):
        account = accounts.Account("101", 1000.0)
        account.withdraw(300.0)
        self.assertEqual(account.balance, 700.0)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0]['type'], 'withdrawal')
        self.assertEqual(account.transactions[0]['amount'], 300.0)

    def test_withdraw_invalid_amount(self):
        account = accounts.Account("112", 500.0)
        with self.assertRaises(ValueError) as context:
            account.withdraw(-50.0)
        self.assertEqual(str(context.exception), "Withdrawal amount must be positive.")

    def test_withdraw_insufficient_funds(self):
        account = accounts.Account("123", 100.0)
        with self.assertRaises(ValueError) as context:
            account.withdraw(200.0)
        self.assertEqual(str(context.exception), "Insufficient funds.")

    def test_buy_shares(self):
        account = accounts.Account("134", 1000.0)
        account.buy_shares("AAPL", 2)
        self.assertEqual(account.balance, 1000.0 - (170.00 * 2))
        self.assertEqual(account.holdings["AAPL"], 2)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0]['type'], 'buy')
        self.assertEqual(account.transactions[0]['symbol'], 'AAPL')
        self.assertEqual(account.transactions[0]['quantity'], 2)
        self.assertEqual(account.transactions[0]['price'], 170.00)

    def test_buy_shares_invalid_quantity(self):
        account = accounts.Account("145", 500.0)
        with self.assertRaises(ValueError) as context:
            account.buy_shares("TSLA", -1)
        self.assertEqual(str(context.exception), "Quantity must be positive.")

    def test_buy_shares_insufficient_funds(self):
        account = accounts.Account("156", 100.0)
        with self.assertRaises(ValueError) as context:
            account.buy_shares("GOOGL", 1)
        self.assertEqual(str(context.exception), "Insufficient funds to buy shares.")

    def test_sell_shares(self):
        account = accounts.Account("167", 5000.0)
        account.buy_shares("AAPL", 5)
        account.sell_shares("AAPL", 2)
        self.assertEqual(account.balance, 5000.0 - (170.00 * 5) + (170.00 * 2))
        self.assertEqual(account.holdings["AAPL"], 3)
        self.assertEqual(len(account.transactions), 2)
        self.assertEqual(account.transactions[1]['type'], 'sell')
        self.assertEqual(account.transactions[1]['symbol'], 'AAPL')
        self.assertEqual(account.transactions[1]['quantity'], 2)
        self.assertEqual(account.transactions[1]['price'], 170.00)

    def test_sell_shares_invalid_quantity(self):
        account = accounts.Account("178", 1000.0)
        account.buy_shares("TSLA", 3)
        with self.assertRaises(ValueError) as context:
            account.sell_shares("TSLA", -1)
        self.assertEqual(str(context.exception), "Quantity must be positive.")

    def test_sell_shares_insufficient_shares(self):
        account = accounts.Account("189", 2000.0)
        account.buy_shares("AAPL", 1)
        with self.assertRaises(ValueError) as context:
            account.sell_shares("AAPL", 2)
        self.assertEqual(str(context.exception), "Insufficient shares to sell.")

    def test_sell_shares_all_shares(self):
        account = accounts.Account("190", 2000.0)
        account.buy_shares("AAPL", 1)
        account.sell_shares("AAPL", 1)
        self.assertTrue("AAPL" not in account.holdings)

    def test_get_portfolio_value(self):
        account = accounts.Account("201", 1000.0)
        account.buy_shares("AAPL", 2)
        account.buy_shares("TSLA", 1)
        expected_value = 1000.0
        self.assertEqual(account.get_portfolio_value(), expected_value)

    def test_get_profit_loss(self):
       account = accounts.Account("212", 1000.0)
       account.buy_shares("AAPL", 1)
       expected_profit_loss = account.get_portfolio_value() - 1000.0
       self.assertEqual(account.get_profit_loss(), 0.0)

    def test_get_holdings(self):
        account = accounts.Account("223", 1000.0)
        account.buy_shares("AAPL", 2)
        holdings = account.get_holdings()
        self.assertEqual(holdings["AAPL"], 2)
        self.assertNotEqual(id(holdings), id(account.holdings))

    def test_get_transactions(self):
        account = accounts.Account("234", 1000.0)
        account.deposit(100.0)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['type'], 'deposit')
        self.assertNotEqual(id(transactions), id(account.transactions))

if __name__ == '__main__':
    unittest.main()
