from datetime import timedelta
from os import stat
import numpy as np
import quantstats as qs

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
        self.wins = []

    def add_trade(self, trade_val):
        """
        This function is used to add the value of trades to the list within the account.
        """
        self.trade_val.append(trade_val)
        if trade_val <= 0:
            change = self.trade_val[-2] + trade_val # if it is 0 or negative means closing trade 
            self.value = self.value + change
            self.account_bal.append(self.value)
        else:
            pass

    def update_balance(self, change):
        """
        This function helps to update the account balance and keep track of the changing balance from day to day
        """
        self.value = self.value + change
        self.account_bal.append(self.value)

    def update_wins(self, change):
        """
        This function updates the number of wins in an account
        """
        self.wins.append(change)

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
        (dataset["DTE"] > dte_min) & (dataset["Strike"] == strike_price)][["oid", "Bid", "Expiration"]].values[0]
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

class BacktestOperations:
    """
    Static holder to store operations for backtesting
    """

    @staticmethod
    def run_backtest(curr_date, dataset, acc_initial_value): # start backtest, with own dataset
        days = []
        curr_account = AccountBal(acc_initial_value)
        tradeOn = False

        while curr_date < dataset["DataDate"].max(): # loop through the days
            curr_date += timedelta(1) # increase days
            days.append(curr_date) # store days
            daily_set = dataset[dataset["DataDate"] == curr_date] # create sub-df with just today's data
            if tradeOn == False: # if there is no trade on, we want to search for a trade
                try:
                    new_trade = Trade(TradeOperations.find_trade(daily_set)) # create new trade class
                    curr_account.add_trade(new_trade.get_value())
                    curr_account.account_bal.append(curr_account.value)
                    tradeOn = True
                except:
                    print(str(curr_date) + " is a Weekend, unable to open")
                    curr_account.account_bal.append(curr_account.value)
                
            elif tradeOn == True:
                try:
                    if new_trade.exp-timedelta(0) == curr_date:
                        new_trade.update_trade(daily_set[daily_set["oid"] == new_trade.id]["Ask"].values[0])
                        curr_account.add_trade(-new_trade.get_value())
                        print(str(curr_date) + " New Trade Added " + str(new_trade.id))
                        new_trade = Trade(TradeOperations.find_trade(daily_set))
                        curr_account.add_trade(new_trade.get_value())
                    else:
                        print(str(curr_date) + " No Trades Running " + str(new_trade.id))
                        curr_account.account_bal.append(curr_account.value)
                    pass
                except:
                    print(str(curr_date) + " ERROR: Closing Trade Manually ")
                    new_trade.update_trade(float(new_trade.get_value())/2)
                    curr_account.add_trade(-new_trade.get_value())
                    tradeOn = False
                        
        return curr_account.trade_val, curr_account.account_bal, days

    @staticmethod
    def benchmark_results(bal, days, benchmark="SPY"):
        """
        Function to allow one to analyse the results of a
        backtest. Requires list of balances and dates from
        backtest results. 

        Default benchmark is SPY but this can be changed. 
        """
        returns_series = pd.DataFrame({"Returns": pd.Series(bal[0:len(days)]).pct_change(), "Date":days}).set_index("Date").squeeze()
        return qs.reports.basic(returns_series, benchmark)
