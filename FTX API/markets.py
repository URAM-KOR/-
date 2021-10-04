import pandas as pd
import requests

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


markets = pd.DataFrame(requests.get('https://ftx.com/api/markets').json()['result'])
print(markets)

# 선물시장 필터링
futures = markets.loc[markets['name'].str.contains('PERP',case=False)]
print(futures.sort_values('change24h',ascending=False).head(3))

