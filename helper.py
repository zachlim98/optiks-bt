from datetime import timedelta
from os import stat
import numpy as np

class Trade: 
    """
    This class handles all trade objects.
    """
    def __init__(self, tradeop):
        self.id = tradeop[0]
        self.value = tradeop[1]
        self.exp = tradeop[2]

    def update_trade(self, value):
        """
        This function is used to update the value of a trade.
        This should be used to close a trade. 
        """
        self.value = value

    def get_value(self):
        return self.value

class AccountBal: 
    """
    This is the Account Balance class which will handle accounts in the simulation. 
    """
    def __init__(self, value):
        self.value = value
        self.trade_val = []
        self.account_bal = []

    def add_trade(self, trade_val):
        """
        This function is used to add the value of trades to the list within the account.
        """
        self.trade_val.append(trade_val)

    def update_balance(self, change):
        """
        This function helps to update the account balance and keep track of the changing balance from day to day
        """
        self.value = self.value + change
        self.account_bal.append(self.value)

class TradeOperations: 
    """
    static storage for various trade operations that
    work on a higher level 
    """
    @staticmethod
    def find_trade(dataset):
        """
        This function is used to find a new trade to enter. It looks for a strike price and sets a DTE range. 
        These two parameters are sufficient to source for the trade to enter. It returns a tuple which 
        is then used within the Trade class to create a new Trade object. 
        """
        strike_price = np.round(dataset["Underlying"].iloc[0])
        dte_max = timedelta(9)
        dte_min = timedelta(6)
        trade_dets = dataset[(dataset["DTE"] < dte_max) & 
        (dataset["DTE"] > dte_min) & (dataset["Strike"] == strike_price) & 
        (dataset["Type"] == "put")][["oid", "Bid", "Expiration"]].values[0]
        trade_oid = trade_dets[0]
        trade_val = trade_dets[1]
        trade_exp = trade_dets[2]
        return trade_oid, trade_val, trade_exp

    @staticmethod
    def close_trade(account, curr_trade, close_val, next_trade):
        """
        This function is used to close a trade and open a new one. It replicates the effect of 
        "rolling"
        """
        account.add_trade(curr_trade.get_value())
        account.update_balance(curr_trade.get_value() - close_val)
        curr_trade.update_trade(close_val)
        account.add_trade(-curr_trade.get_value())
        account.add_trade(next_trade.get_value())
