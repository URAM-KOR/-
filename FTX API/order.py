import Login
import requests
import pandas as pd
import json
import time
from time import sleep
import datetime
import ccxt
import ftx


# for i in markets.targetList:
#     coin = f'{i}'
# coin = input("input Market \n")
# print('Market :', coin)

while True:
    today = datetime.datetime.today()
    today = time.mktime(today.timetuple())

    Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
    Previous_Date = time.mktime(Previous_Date.timetuple())
    # Second as a decimal number [00,61] (or Unix Timestamp)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    markets = pd.DataFrame(requests.get('https://ftx.com/api/markets').json()['result'])
    # 선물시장 필터링
    futures = markets.loc[markets['name'].str.contains('PERP', case=False)]
    futures = futures[futures['volumeUsd24h'] > 10000000]
    targetList = futures.sort_values('changeBod', ascending=False)['name'].head(3)
    # need = pd.Series(['BTC-PERP', 'ETH-PERP'])
    # targetList = pd.concat([targetList, need])

    try:

        for i in targetList:
            coin = i

            # BALANCE
            c = ccxt.ftx({
                'apiKey': 'VYXBrkmuhutN9cr2APKbblqW4esKX-0Euhe9evr4',
                'secret': 'QUsJaE8upSSdP9Rve1DRPEeGdcMMEUP-f2iIXiAO',
                'enableRateLimit': True,
                # 'headers': {'FTX-SUBACCOUNT': 'bot'}, # uncomment line if using subaccount
            })

            balance = pd.DataFrame(c.fetch_balance())
            balance = float(balance['total']['USD'])
            position = pd.DataFrame(c.fetch_positions())
            position = position.set_index('future')
            BTC = position[position.index == f"{coin}"]['size'].apply(pd.to_numeric, errors='ignore')
            wallet = pd.DataFrame(c.fetch_account_positions()).apply(pd.to_numeric, errors='ignore')
            wallet = wallet[wallet['size'] > 0]
            print(wallet)



            # STRATEGY
            c = ftx.FtxClient(api_key="VYXBrkmuhutN9cr2APKbblqW4esKX-0Euhe9evr4",
                              api_secret="QUsJaE8upSSdP9Rve1DRPEeGdcMMEUP-f2iIXiAO")
            historical = requests.get(
                'https://ftx.com/api/markets/{}/candles?resolution=900&start_time=1609462800'.format(coin)).json()
            historical = pd.DataFrame(historical['result'])

            recent = requests.get(
                'https://ftx.com/api/markets/{}/candles?resolution=15&start_time=1609462800'.format(coin)).json()
            recent = pd.DataFrame(recent['result'])
            recent = recent.loc[:, ['open', 'close', 'high', 'low']].iloc[-1]['open']
            ma_20 = historical['close'].tail(20).mean()
            historical = historical.loc[:, ['open', 'close', 'high', 'low']]


            X = 0.5
            print('''-----------------------------------------------
            Market :''', coin)
            print(historical.tail(3))
            print('-----------------------------------------------')
            print('잔액 =', balance, 'USD')
            print('미결제:', BTC[0])
            print('현재시각 =',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            # print(float(datetime.datetime.now().strftime('%M'))%15)
            T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
            T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X


            try:
                print("레버리지 =", BTC[0]/(balance / recent), "배")
                print(f"현재가 = {recent:.8f}")
                T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
                print('매수기준 =', T1,'>',ma_20)
                print('매도기준 =',(historical.iloc[-1]['open'] - 0.2 * (historical.iloc[-2]['high']-historical.iloc[-2]['low'])))
            except Exception as e:
                print(f'Error obtaining {coin} old data: {e}')
                # 매수조건
            if recent >= T1 > ma_20:
                # if (historical.iloc[-1]['open'] - historical.iloc[-2]['open']) < 0:
                #     if float(datetime.datetime.now().strftime('%S')) > 30 and float(datetime.datetime.now().strftime('%M')) % 15 > 0 :
                        T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
                        # print('매수기준 =', T1)
                        # T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
                        # print('매도기준 =', T2)
                        if BTC[0] * recent < 0.4*balance:
                            try:
                                if coin == ('BTC-PERP' or 'ETH-PERP'):
                                    r = c.place_order(f'{coin}', "buy", size =  3 * balance / recent,
                                                      type='market',
                                                      client_id=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                    print(r)

                                print('----------------매수실행-----------------------')
                                print('매수기준 =', T1, '현재가=', recent)

                                r = c.place_order(f'{coin}', "buy",
                                                      type='market',
                                                  size = 0.5 * balance / recent,
                                                  client_id=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                print(r)

                            except Exception as e:
                                print(f' buying failed{e}')
                        else:
                            print('balance was not satisfied.')
                        sleep(2)
            else:
                print('The buy requirement was not satisfied.')
            sleep(2)

            #매도조건


            # if float(datetime.datetime.now().strftime('%M')) % 15 == 0:
            #     if float(datetime.datetime.now().strftime('%S')) < 30:
                    # T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
                    # print('매수기준 =', T1)
                    # T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
                    # print('매도기준 =', T2)

            for w in wallet['future']:
                w_hist = requests.get(
                    f'https://ftx.com/api/markets/{w}/candles?resolution=900&start_time=1609462800'.format(
                        coin)).json()
                w_hist = pd.DataFrame(w_hist['result'])
                w_hist = w_hist.loc[:, ['open', 'close', 'high', 'low']]
                w_recent = requests.get(
                    f'https://ftx.com/api/markets/{w}/candles?resolution=15&start_time=1609462800'.format(
                        coin)).json()
                w_recent = pd.DataFrame(w_recent['result'])
                w_recent = w_recent.loc[:, ['open', 'close', 'high', 'low']].iloc[-1]['open']

                if (w_hist.iloc[-1]['open'] - 0.2 * (w_hist.iloc[-2]['high']-w_hist.iloc[-2]['low'])) > w_recent:
                    print('----------------매도실행-----------------------')
                    print('매도기준=',(w_hist.iloc[-1]['open'] - 0.2 * (w_hist.iloc[-2]['high']-w_hist.iloc[-2]['low'])),'현재가=', w_recent)
                    print(float(wallet[wallet['future']==w]['size']))
                    s = c.place_order(f'{w}', "sell", type='market', size = float(wallet[wallet['future'] == w]['size']), reduce_only=True, client_id=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    print(s)
                    sleep(1)

            print('-----------------------------------------------')
    except Exception as e:
        print(f'{e}??')