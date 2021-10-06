import Login
import requests
import pandas as pd
import json
from time import sleep
import datetime
import ccxt
import ftx


# for i in markets.targetList:
#     coin = f'{i}'
# coin = input("input Market \n")
# print('Market :', coin)

while True:
    import markets
    for i in markets.targetList:
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
        print('잔액 =', balance, 'USD')
        print('미체결:', BTC[0])
        print('현재시각 =',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # print(float(datetime.datetime.now().strftime('%M'))%15)
        T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
        T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X

        try:
            print("레버리지 =", BTC[0]/(balance / recent), "배")
            print(f"현재가 = {recent:.8f}")
            T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
            print('매수기준 =', T1)
        except Exception as e:
            print(f'Error obtaining {coin} old data: {e}')
        #매수조건
        if recent >= T1 >ma_20:
            if float(datetime.datetime.now().strftime('%S')) > 30:
                T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
                # print('매수기준 =', T1)
                # T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
                # print('매도기준 =', T2)
                if BTC[0]*recent < 0.2 * balance:
                    r = c.place_order(f'{coin}', "buy", 1.01*recent, 0.2*balance/recent, client_id =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    print(r)
                else: print('balance was not satisfied.')
                sleep(2)
            else:
                print('time was not satisfied.')
            sleep(2)
        #매도조건

        if float(datetime.datetime.now().strftime('%M')) % 15 == 0:
            if float(datetime.datetime.now().strftime('%S')) < 30:
                # T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
                # print('매수기준 =', T1)
                # T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
                # print('매도기준 =', T2)
                for w in wallet['future']:
                    s = c.place_order(f'{w}', "sell", 0.99*recent, wallet[wallet['future']==w]['size'], reduce_only=True,
                                      client_id=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print(s)
                sleep(2)
        else: print('The buy requirement was not satisfied.')