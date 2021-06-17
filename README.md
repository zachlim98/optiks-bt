

![Backtester](X:\GitHub\optiks-bt\resources\logo.png)

![issues](https://img.shields.io/github/issues/zachlim98/optiks-bt) ![license](https://img.shields.io/github/license/zachlim98/optiks-bt)



## OpTiks Backtester

### What is OpTiks?

OpTiks is an attempt to create an options backtester that is simple and elegant. It is designed to work simply based off the Pandas framework. It is currently still very much in a developmental stage and there is still much to be done. Most option backtesting systems available online backtest using delta as selection criterion - OpTiks is designed to work on more than just delta selection and allow for specific selection based on more criteria. 

### How does it work?

The key idea behind OpTiks is that one will be able to test option strategies with their own data and without the need to work with complicated databases or storage systems. There are two key concepts behind OpTiks.

1. Every day is a different day

   The code runs by chunking up the data into days. We create a new pandas dataframe for each separate day and then look for the option within that day (e.g. look for specific delta trades or look for specific strike prices/expirations). This allows is to be more efficient than working with an entire dataset which may have upwards of 15 million rows of data. Instead, even for the ticker with the most populous option set (SPY), each dataframe is minimized to ~40,000 rows which runs more efficiently. 

2. Each trade is unique.

   Each option is given a unique identifier based on a combination of strike and expiry. This allows us to easily identify each option within a given day and calculate the gains/losses for a particular trade. Each option trade is its own object with its own attributes (strike, exp, value) and this is used to compare against the individual day dataframe that is generated. 

The main function is `run_backtest()` which, as the name suggests, runs the backtest. The main strategy function is currently `find_trade()` which, as explained below, only works for a single strategy. More strategies will be slowly added. 

### What can it do?

Currently OpTiks is designed to test only a single strategy - an ATM (At-The-Money) put writing strategy with no trade management. The developmental roadmap is below with the future strategies will be added. OpTiks rides on [quantstats](https://github.com/ranaroussi/quantstats) to allow for analysis of the strategy. This is an example output from OpTiks (using SPY data, 2019 - 2021), with benchmark as buy-and-hold SPY

<img src="C:\Users\Zachary\AppData\Roaming\Typora\typora-user-images\image-20210617112647043.png" alt="image-20210617112647043" style="zoom: 50%;" />

### Strategy Roadmap

- ATM put writing (hold strike, no rolling)
- Hedging (e.g. VXX calls)
- Wheeling (taking assignment and call writing)