import pandas as pd
import requests

orderbook = requests.get('https://ftx.com/api/markets/BTC-PERP/orderbook').json()

orderbook_asks = pd.DataFrame(orderbook['result']['asks'])
orderbook_bids = pd.DataFrame(orderbook['result']['bids'])

df = pd.merge(orderbook_bids , orderbook_asks , left_index=True, right_index=True)
df = df.rename({"0_x":"Bid Price","1_x":"Bid Amount",
                "0_y":"Ask Price","1_y":"Ask Amount"}, axis='columns')
print(df.head())