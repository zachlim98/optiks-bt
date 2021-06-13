from fuctions import Trade, AccountBal, TradeOperations
from datetime import timedelta
from datetime import date
import pandas as pd

# read the pickle file and create a sample day
truncated = pd.read_pickle("truncated.pickle")
sample_day = truncated[truncated["DataDate"] == truncated["DataDate"].min()]

curr_trade = TradeOperations.find_trade(sample_day)
my_account = AccountBal(100)
next_trade = Trade("SPY2019-06-17P290", 2.40, date(2019, 6, 17))
TradeOperations.close_trade(my_account, curr_trade, 0.40, next_trade)
curr_trade = next_trade

print(my_account.trade_val)
print(my_account.account_bal)
