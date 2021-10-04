import Login
import requests
import pandas as pd
import json
from time import sleep
import datetime
import ccxt
import ftx


while True:
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
    BTC = float(position[position.index == 'BTC-PERP']['size'])

    sleep(2)

    # STRATEGY
    c = ftx.FtxClient(api_key="VYXBrkmuhutN9cr2APKbblqW4esKX-0Euhe9evr4",
                      api_secret="QUsJaE8upSSdP9Rve1DRPEeGdcMMEUP-f2iIXiAO")
    historical = requests.get(
        'https://ftx.com/api/markets/BTC-PERP/candles?resolution=900&start_time=1609462800').json()
    historical = pd.DataFrame(historical['result'])
    historical = historical.loc[:, ['open', 'close', 'high', 'low']]

    X = 0.5

    print(historical.tail(3))
    print('잔액 =', balance, 'USD')
    print('미체결:', BTC)
    print('현재시각 =',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # print(float(datetime.datetime.now().strftime('%M'))%15)
    T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
    T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X

    try:
        btc_data = requests.get('https://ftx.com/api/markets/BTC-PERP').json()
        print(f"레버리지 ={BTC/(balance / btc_data['result']['ask']):.2f} 배")
        print('현재가 =', btc_data['result']['ask'])
    except Exception as e:
        print(f'Error obtaining BTC old data: {e}')

    if BTC != 0:
        if btc_data['result']['ask'] < T2:
        # if float(datetime.datetime.now().strftime('%M'))%15==0:
            T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
            print('매수기준 =', T1)
            T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
            print('매도기준 =', T2)
            s = c.place_order("BTC-PERP", "sell", 1,  0.0001, reduce_only=True, client_id =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(s)
            sleep(2)
        else:
            T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
            print('매수기준 =', T1)
            T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
            print('매도기준 =', T2)
            print('The trade requirement was not satisfied.')
    elif btc_data['result']['ask'] < T1:
        T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
        print('매수기준 =', T1)
        T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
        print('매도기준 =', T2)
        print('The trade requirement was not satisfied.')
        sleep(2)
        continue

    elif btc_data['result']['ask'] >= T1:
        try:
            T1 = historical.iloc[-1]['open'] + (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
            print('매수기준 =', T1)
            T2 = historical.iloc[-1]['open'] - (historical.iloc[-2]['high'] - historical.iloc[-2]['low']) * X
            print('매도기준 =', T2)
            r = c.place_order("BTC-PERP", "buy", btc_data['result']['ask'], 0.0001,client_id =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(r)
        except Exception as e:
            print(f'Error making order request: {e}')
        sleep(2)


