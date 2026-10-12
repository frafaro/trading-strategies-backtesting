# Trading Strategies & Vectorized Backtesting

Strategie di trading algoritmico e backtesting vettorizzato, basati su *Python for Algorithmic Trading* di Yves Hilpisch.

## Moduli (strategie)

| File | Strategia |
|---|---|
| `SMAVectorBacktester.py` | Incrocio di medie mobili semplici (SMA crossover), con ottimizzazione brute-force dei parametri |
| `MomVectorBacktester.py` | Momentum / time-series momentum |
| `MRVectorBacktester.py` | Mean reversion |
| `sma_homework_lezione3.py` | Compito a casa: variante del backtester SMA |

Ogni modulo è eseguibile direttamente (`python SMAVectorBacktester.py`) grazie al blocco `if __name__ == '__main__'`.

## Notebook

- **`Vectorized_backtesting.ipynb`** — costruisce le tre strategie **passo passo** (definizione della posizione, calcolo dei rendimenti, drawdown, ecc.); include anche un esempio su dati intraday (`SPX_1min_05052020.csv`).
  > Nota: la sezione teorica iniziale "Making Use of Vectorization" (NumPy e pandas) è stata spostata nella repo `python-basics`, notebook `theory_data_structures.ipynb` — qui resta solo la parte pratica su strategie e backtesting.
- **`Generalized_backtesting.ipynb`** — raccoglie le sezioni "Generalizing the Approach" delle tre strategie: applica direttamente le classi dei moduli `.py` (SMA, Momentum, Mean-Reversion) per eseguire i backtest in poche righe, inclusa l'ottimizzazione dei parametri (built-in per SMA, brute force per Mean-Reversion).
- **`ProvaEsameBande.ipynb`** — strategia mean-reversion con bande di Bollinger (prova d'esame).

## Dati

- `pyalgo_eikon_eod_data.csv` — copia locale dei dati EOD usati dai moduli (gli script la scaricano anche da `http://hilpisch.com/pyalgo_eikon_eod_data.csv`).
- `SPX_1min_05052020.csv` — dati S&P 500 a 1 minuto (5 maggio 2020).

> Nota: i moduli leggono i dati dall'URL di hilpisch.com, quindi serve una connessione Internet. In alternativa si può modificare `get_data()` per usare la copia locale del CSV.

## Requisiti

```
pandas, numpy, scipy, matplotlib
```

Ambiente consigliato: conda `arima` (vedi la repo `interactive-brokers-api`, file `arima.yml`).

- **Notebook**: selezionare il kernel **arima** nell'editor — non serve attivare l'ambiente nel terminale.
- **Script .py da terminale**: prima eseguire `conda activate arima`.
- **Non serve TWS/Interactive Brokers**: basta la connessione Internet per scaricare i dati da hilpisch.com (oppure usare i CSV locali).
