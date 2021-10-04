import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

df = pd.read_csv('stockdata.csv', index_col=0, parse_dates=True)
df.index.name = 'Date'
mpf.plot(df,type='candle', mav=(10,20,60),volume=True)