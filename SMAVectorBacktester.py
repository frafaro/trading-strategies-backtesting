#
# Python Module with Class
# for Vectorized Backtesting
# of SMA-based Strategies
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import numpy as np
import pandas as pd
from scipy.optimize import brute

#The (object) part is considered optional in Python 3 and later versions. In Python 2, it was more common to see explicit inheritance from object to create new-style classes.
class SMAVectorBacktester(object):
    ''' Class for the vectorized backtesting of SMA-based trading strategies.

    Attributes
    ==========
    symbol: str
        RIC symbol with which to work with
    SMA1: int
        time window in days for shorter SMA
    SMA2: int
        time window in days for longer SMA
    start: str
        start date for data retrieval
    end: str
        end date for data retrieval

    Following methods are for this class defined and can be used
    =======
    get_data:
        retrieves and prepares the base data set
    set_parameters:
        sets one or two new SMA parameters
    run_strategy:
        runs the backtest for the SMA-based strategy
    plot_results:
        plots the performance of the strategy compared to the symbol
    update_and_run:
        updates SMA parameters and returns the (negative) absolute performance
    optimize_parameters:
        implements a brute force optimizeation for the two SMA parameters
    '''

    def __init__(self, symbol, SMA1, SMA2, start, end):
        ''' 
        automatically executed when we call an object of the class.
        ex: smabt = SMAVectorBacktester('EUR=', 42, 252, '2010-1-1', '2020-12-31')
        self is used in order to be able to compute the backtesting even with different data
        '''
        self.symbol = symbol #receive EUR= 
        self.SMA1 = SMA1 #42
        self.SMA2 = SMA2 #252
        self.start = start #'2010-1-1'
        self.end = end #'2020-12-31'
        self.results = None
        self.get_data() #recall the function below for the dataset

    def get_data(self):
        ''' Retrieves and prepares the data.
        '''
        raw = pd.read_csv('http://hilpisch.com/pyalgo_eikon_eod_data.csv',
                          index_col=0, parse_dates=True).dropna() #first column contains the date it used as index, so if you use a different dataset remember this
        raw = pd.DataFrame(raw[self.symbol]) #select the column corrisponding to the symble and transfors it in a dataframe
        raw = raw.loc[self.start:self.end] #use the same range of dates as in the csv
        raw.rename(columns={self.symbol: 'price'}, inplace=True) #replace the name of the tickets with 'price' 
        raw['return'] = np.log(raw / raw.shift(1)) #crete column for log returns
        raw['SMA1'] = raw['price'].rolling(self.SMA1).mean() #sma1 with the number defined in __init__
        raw['SMA2'] = raw['price'].rolling(self.SMA2).mean() #sma2
        self.data = raw #the dataframe is saved in data

    def set_parameters(self, SMA1=None, SMA2=None):
        ''' 
        this allows to change SMA1 and SMA2 without ricreating the object and downloading the data every time
        but to run the strategy with new SMAs we need to recall run_strategy
        '''
        if SMA1 is not None:
            self.SMA1 = SMA1
            self.data['SMA1'] = self.data['price'].rolling(
                self.SMA1).mean()
        if SMA2 is not None:
            self.SMA2 = SMA2
            self.data['SMA2'] = self.data['price'].rolling(
                self.SMA2).mean()

    def run_strategy(self):
        ''' 
        Backtests the trading strategy.
        '''
        data = self.data.copy().dropna() #create a copy (to not modify self.data) and drop NA values of the dataframe
        data['position'] = np.where(data['SMA1'] > data['SMA2'], 1, -1) #define the position
        data['strategy'] = data['position'].shift(1) * data['return'] #calculates the return of the strategy
        data.dropna(inplace=True) #replace Nan agin cause the returnes are shifted by 1 so the first line is Nan
        data['creturns'] = data['return'].cumsum().apply(np.exp) #cumulative returns of the asset
        data['cstrategy'] = data['strategy'].cumsum().apply(np.exp) #cumulative returns of the startegy
        self.results = data #the final dataframe is memorised in results so it can be used also by plot_results
        # gross performance of the strategy, i.e. not taking slippage and trading costs into account
        aperf = data['cstrategy'].iloc[-1] #-1 take the last value of the series since it's cumulative 
        # delta performance of strategy, i.e. returns of the strategy minus the benchmark
        operf = aperf - data['creturns'].iloc[-1]
        return round(aperf, 2), round(operf, 2)

    def plot_results(self):
        ''' 
        Plots the cumulative performance of the trading strategy
        compared to the symbol.
        '''
        if self.results is None:
            print('No results to plot yet. Run a strategy.')
        title = '%s | SMA1=%d, SMA2=%d' % (self.symbol,
                                               self.SMA1, self.SMA2)
        self.results[['creturns', 'cstrategy']].plot(title=title, #select the two series to be visualised one of the strategy the other of the asset (buy and hold is the benchmark)
                                                     figsize=(10, 6))

    def update_and_run(self, SMA): 
        ''' Updates SMA parameters and returns negative absolute performance
        (for minimazation algorithm).

        the brute algo is used to minimiz the objective function, our goal is to maximize it so
        we give the result with the negative sign
        '''
        self.set_parameters(int(SMA[0]), int(SMA[1]))
        return -self.run_strategy()[0] #first element of run_strutegy that is the performance

    def optimize_parameters(self, SMA1_range, SMA2_range):
        ''' 
        Finds global maximum given the SMA parameter ranges.
        for each combination brute performs:
        - recall update_and_run
        - update the SMAs
        - execute the backtest
        - evaluate the objective function
        - store the combination who minimizes the negative values

        '''
        #optimizes based on the scipy.optimize package
        opt = brute(self.update_and_run, (SMA1_range, SMA2_range), finish=None)
        #the optimal/best parameters will be returned
        return opt, -self.update_and_run(opt)

'''
The line if __name__ == '__main__': is a common idiom used in Python to check whether a script is being executed as the main program or being imported as a module.
When a Python script is executed, the special variable __name__ is set to '__main__' by default. 
However, when a script is imported as a module into another script, the value of __name__ is set to the name of the module instead of '__main__'.
The line if __name__ == '__main__': checks if the value of __name__ is equal to '__main__', indicating that the script is being run as the main program.
The code block that follows, usually indented, contains the main code or the entry point of the script. 
This code will only be executed if the script is run directly as the main program, and it will be skipped if the script is imported as a module.
'''
if __name__ == '__main__':
    smabt = SMAVectorBacktester('EUR=', 42, 252,
                                '2010-1-1', '2020-12-31')
    print(smabt.run_strategy())
    smabt.set_parameters(SMA1=20, SMA2=100)
    print(smabt.run_strategy())
    print(smabt.optimize_parameters((30, 56, 4), (200, 300, 4)))
