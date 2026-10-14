# Trading Strategies & Vectorized Backtesting

Algorithmic trading strategies and vectorized backtesting, based on *Python for Algorithmic Trading* by Yves Hilpisch.

## Workflow

The repository follows a three-step progression:

1. **`step_by_step_backtesting.ipynb`** :  builds each strategy **from scratch**, step by step. Three strategies are covered:
   - **SMA crossover** (Simple Moving Averages): long when the faster SMA is above the slower one, short otherwise.
   - **Momentum** (time-series momentum): position given by the sign of the rolling mean of recent returns.
   - **Mean reversion**: trades the distance between the price and its SMA, entering when it exceeds a threshold.

   For each strategy the notebook computes, briefly: data loading and log returns, position definition (vectorized with `np.where` / `np.sign`), strategy returns (lagged position × return), cumulative performance vs. the buy-and-hold benchmark, and drawdowns. It also includes an example on intraday data (`SPX_1min_05052020.csv`).

2. **The `.py` modules** :  automate the whole process by wrapping each strategy in a class (data retrieval, backtest, plotting), and also introduce **parameter optimization**:

   | File | Strategy |
   |---|---|
   | `SMAVectorBacktester.py` | SMA crossover, with built-in brute-force optimization of the two SMA windows |
   | `MomVectorBacktester.py` | Momentum, with the momentum lag as parameter and proportional transaction costs |
   | `MRVectorBacktester.py` | Mean reversion (inherits from the momentum class), parametrized by SMA window and threshold |
   
   Each module can be run directly (`python SMAVectorBacktester.py`) thanks to the `if __name__ == '__main__'` block.

3. **`Generalized_backtesting.ipynb`** : recalls the classes/functions defined in the `.py` modules and plays with them: it runs the backtests in a few lines, compares results with and without transaction costs, and performs parameter optimization (built-in for SMA, a brute-force loop for mean reversion).

## Data

- `pyalgo_eikon_eod_data.csv` — local copy of the EOD data used by the modules (the scripts also download it from `http://hilpisch.com/pyalgo_eikon_eod_data.csv`).
- `SPX_1min_05052020.csv` — S&P 500 1-minute data (May 5, 2020).

> Note: the modules read the data from the hilpisch.com URL, so an Internet connection is required. Alternatively, `get_data()` can be modified to use the local CSV copy.

## Requirements

```
pandas, numpy, scipy, matplotlib
```

Recommended environment: conda `arima` (see the `interactive-brokers-api` repo, file `arima.yml`).

- **Notebooks**: select the **arima** kernel in the editor ,  no need to activate the environment in the terminal.
- **`.py` scripts from the terminal**: run `conda activate arima` first.
- **No TWS/Interactive Brokers needed**: an Internet connection is enough to download the data from hilpisch.com (or use the local CSVs).
