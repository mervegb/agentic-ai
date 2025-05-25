# app.py
import gradio as gr
from accounts import Account, get_share_price

# Initialize the account
account = Account("user123", initial_deposit=10000.0)

def deposit(amount):
    try:
        amount = float(amount)
        account.deposit(amount)
        return get_account_state()
    except ValueError as e:
        return str(e), account.balance, account.get_portfolio_value(), account.get_profit_loss(), account.get_holdings(), account.get_transactions()

def withdraw(amount):
    try:
        amount = float(amount)
        account.withdraw(amount)
        return get_account_state()
    except ValueError as e:
        return str(e), account.balance, account.get_portfolio_value(), account.get_profit_loss(), account.get_holdings(), account.get_transactions()

def buy_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        account.buy_shares(symbol, quantity)
        return get_account_state()
    except ValueError as e:
        return str(e), account.balance, account.get_portfolio_value(), account.get_profit_loss(), account.get_holdings(), account.get_transactions()

def sell_shares(symbol, quantity):
    try:
        quantity = int(quantity)
        account.sell_shares(symbol, quantity)
        return get_account_state()
    except ValueError as e:
        return str(e), account.balance, account.get_portfolio_value(), account.get_profit_loss(), account.get_holdings(), account.get_transactions()

def get_account_state():
    return "", account.balance, account.get_portfolio_value(), account.get_profit_loss(), account.get_holdings(), account.get_transactions()

with gr.Blocks() as demo:
    gr.Markdown("# Simple Trading Account")

    with gr.Column():
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit")

        withdraw_amount = gr.Number(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw")

        buy_symbol = gr.Text(label="Buy Symbol")
        buy_quantity = gr.Number(label="Buy Quantity")
        buy_button = gr.Button("Buy Shares")

        sell_symbol = gr.Text(label="Sell Symbol")
        sell_quantity = gr.Number(label="Sell Quantity")
        sell_button = gr.Button("Sell Shares")

    error_message = gr.Text(label="Error Message")
    balance = gr.Number(label="Balance")
    portfolio_value = gr.Number(label="Portfolio Value")
    profit_loss = gr.Number(label="Profit/Loss")
    holdings = gr.Json(label="Holdings")
    transactions = gr.Json(label="Transactions")

    deposit_button.click(deposit, inputs=deposit_amount, outputs=[error_message, balance, portfolio_value, profit_loss, holdings, transactions])
    withdraw_button.click(withdraw, inputs=withdraw_amount, outputs=[error_message, balance, portfolio_value, profit_loss, holdings, transactions])
    buy_button.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=[error_message, balance, portfolio_value, profit_loss, holdings, transactions])
    sell_button.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=[error_message, balance, portfolio_value, profit_loss, holdings, transactions])

    # Initialize display
    demo.load(get_account_state, outputs=[error_message, balance, portfolio_value, profit_loss, holdings, transactions])

demo.launch()
