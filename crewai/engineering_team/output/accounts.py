
# accounts.py
import datetime

def get_share_price(symbol):
    """
    Retrieves the current price of a share.  This is a mock implementation
    for testing purposes.  In a real system, this would fetch data from
    a market data provider.

    Args:
        symbol (str): The stock symbol (e.g., AAPL, TSLA, GOOGL).

    Returns:
        float: The current price of the share.
    """
    if symbol == "AAPL":
        return 170.00
    elif symbol == "TSLA":
        return 250.00
    elif symbol == "GOOGL":
        return 2700.00
    else:
        return 100.00  # Default price for unknown symbols


class Account:
    """
    Represents a user's trading account.
    """

    def __init__(self, account_id, initial_deposit=0.0):
        """
        Initializes a new Account object.

        Args:
            account_id (str): A unique identifier for the account.
            initial_deposit (float, optional): The initial deposit amount. Defaults to 0.0.
        """
        self.account_id = account_id
        self.balance = initial_deposit
        self.holdings = {}  # {symbol: quantity}
        self.transactions = []  # List of transaction dictionaries
        self.initial_deposit = initial_deposit

    def deposit(self, amount):
        """
        Deposits funds into the account.

        Args:
            amount (float): The amount to deposit.

        Raises:
            ValueError: If the amount is not positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self._record_transaction("deposit", amount=amount)

    def withdraw(self, amount):
        """
        Withdraws funds from the account.

        Args:
            amount (float): The amount to withdraw.

        Raises:
            ValueError: If the amount is not positive or if insufficient funds are available.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self._record_transaction("withdrawal", amount=amount)

    def buy_shares(self, symbol, quantity):
        """
        Buys shares of a given stock.

        Args:
            symbol (str): The stock symbol.
            quantity (int): The number of shares to buy.

        Raises:
            ValueError: If the quantity is not positive or if insufficient funds are available.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        price_per_share = get_share_price(symbol)
        cost = price_per_share * quantity
        if self.balance < cost:
            raise ValueError("Insufficient funds to buy shares.")

        self.balance -= cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity

        self._record_transaction("buy", symbol=symbol, quantity=quantity, price=price_per_share)

    def sell_shares(self, symbol, quantity):
        """
        Sells shares of a given stock.

        Args:
            symbol (str): The stock symbol.
            quantity (int): The number of shares to sell.

        Raises:
            ValueError: If the quantity is not positive or if the account does not hold enough shares.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Insufficient shares to sell.")

        price_per_share = get_share_price(symbol)
        revenue = price_per_share * quantity

        self.balance += revenue
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]

        self._record_transaction("sell", symbol=symbol, quantity=quantity, price=price_per_share)

    def get_portfolio_value(self):
        """
        Calculates the total value of the user's portfolio.

        Returns:
            float: The total portfolio value (cash + value of holdings).
        """
        portfolio_value = self.balance
        for symbol, quantity in self.holdings.items():
            portfolio_value += get_share_price(symbol) * quantity
        return portfolio_value

    def get_profit_loss(self):
        """
        Calculates the profit or loss from the initial deposit.

        Returns:
            float: The profit or loss.
        """
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self):
        """
        Returns the current holdings of the user.

        Returns:
            dict: A dictionary of symbol: quantity representing current holdings.
        """
        return self.holdings.copy() # Return a copy to prevent modification

    def get_transactions(self):
        """
        Returns a list of all transactions for the account.

        Returns:
            list: A list of transaction dictionaries.
        """
        return self.transactions.copy()  # Return a copy to prevent external modification

    def _record_transaction(self, transaction_type, **kwargs):
        """
        Records a transaction in the transaction history.

        Args:
            transaction_type (str): The type of transaction (e.g., "deposit", "buy", "sell").
            **kwargs:  Keyword arguments containing transaction-specific details (e.g., amount, symbol, quantity, price).
        """
        transaction = {
            "type": transaction_type,
            "timestamp": datetime.datetime.now(),
            **kwargs,
        }
        self.transactions.append(transaction)
