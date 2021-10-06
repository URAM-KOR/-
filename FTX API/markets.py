import pandas as pd
import requests
import datetime
import time

# yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
today = datetime.datetime.today()
today = time.mktime(today.timetuple())

Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
Previous_Date = time.mktime(Previous_Date.timetuple())
#Second as a decimal number [00,61] (or Unix Timestamp)

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


markets = pd.DataFrame(requests.get('https://ftx.com/api/markets').json()['result'])
print(markets)

# 선물시장 필터링
futures = markets.loc[markets['name'].str.contains('PERP',case=False)]
print(futures.sort_values('change1h',ascending=False).head(3))

# targetList=[]
# for i in futures['name']:
#     recent = requests.get(f'https://ftx.com/api/markets/{i}/candles?resolution=15&start_time={Previous_Date}').json()
#     recent = pd.DataFrame(recent['result'])
#     recent = recent.loc[:, ['open', 'close', 'high', 'low']].iloc[-1]['open']
#     change_day = requests.get(
#                 f'https://ftx.com/api/markets/{i}/candles?resolution=86400&start_time={Previous_Date}').json()
#     change_day = pd.DataFrame(change_day['result'])
#     change_day = change_day.loc[:, ['open', 'close', 'high', 'low']]
#     change_day['name'] = i
#     change_day['change_day'] = (change_day['open']-recent)/change_day['open']
#     targetList.append(change_day)
#
# targetList = pd.dataFrame(targetList)
# print('tttttttttttttttt',targetList)

targetList = futures.sort_values('changeBod',ascending=False)['name'].head(3)

need = pd.Series(['BTC-PERP','ETH-PERP'])

targetList = pd.concat([targetList,need])

for i in targetList:
    print(i)