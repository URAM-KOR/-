import pandas as pd
import requests

historical = requests.get('https://ftx.com/api/markets/BTC-PERP/candles?resolution=900&start_time=1609462800').json()
historical = pd.DataFrame(historical['result'])
historical.drop(['startTime'], axis = 1, inplace=True)
print(historical.head())

historical['time'] = pd.to_datetime(historical['time'], unit='ms')
historical.set_index('time', inplace=True)
historical['20 SMA'] = historical.close.rolling(20).mean()
print(historical.tail())


#차트
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(x = historical.index,
                                    open = historical['open'],
                                    high = historical['high'],
                                    low = historical['low'],
                                    close = historical['close'],
                                    ),
                     go.Scatter(x=historical.index, y=historical['20 SMA'], line=dict(color='purple', width=1))])


fig.show()