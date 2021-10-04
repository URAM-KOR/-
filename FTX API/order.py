import Login
import requests
import pandas as pd
import json
from time import sleep
import datetime
import ccxt
import ftx

#BALANCE
c = ccxt.ftx({
    'apiKey': 'VYXBrkmuhutN9cr2APKbblqW4esKX-0Euhe9evr4',
    'secret': 'QUsJaE8upSSdP9Rve1DRPEeGdcMMEUP-f2iIXiAO',
    'enableRateLimit': True,
    #'headers': {'FTX-SUBACCOUNT': 'bot'}, # uncomment line if using subaccount
})
balance = pd.DataFrame(c.fetch_balance())
balance = float(balance['total']['USD'])
print('Balance:',balance,'USD')

while True:

    # STRATEGY
    c = ftx.FtxClient(api_key="VYXBrkmuhutN9cr2APKbblqW4esKX-0Euhe9evr4",
                      api_secret="QUsJaE8upSSdP9Rve1DRPEeGdcMMEUP-f2iIXiAO")
    historical = requests.get(
        'https://ftx.com/api/markets/BTC-PERP/candles?resolution=900&start_time=1609462800').json()
    historical = pd.DataFrame(historical['result'])
    historical = historical.loc[:, ['open', 'close', 'high', 'low']]

    X = 0.5
    T1 = historical.iloc[-1]['open'] + (historical.iloc[-1]['high'] - historical.iloc[-1]['low']) * X

    print(historical.tail)

    print('현재시각 =',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('목표가 =', T1)


    try:
        btc_data = requests.get('https://ftx.com/api/markets/BTC-PERP').json()
        print('현재가 =',btc_data['result']['ask'])
        print(balance / btc_data['result']['ask'])

    except Exception as e:
        print(f'Error obtaining BTC old data: {e}')

    if datetime.datetime.now().strftime('%M')==0 or 15 or 30 or 45:
        s = c.place_order("BTC-PERP", "sell", 1,  5 * balance/btc_data['result']['ask'], True)
        print(s)

    if btc_data['result']['ask'] < T1:
        print('The trade requirement was not satisfied.')
        sleep(2)
        continue

    elif btc_data['result']['ask'] >= T1:
        try:
            r = c.place_order("BTC-PERP", "buy", btc_data['result']['ask'], 5*balance/btc_data['result']['ask'])
            print(r)
        except Exception as e:
            print(f'Error making order request: {e}')

        sleep(2)

        try:
            check = c.get_open_orders(r)
        except Exception as e:
            print(f'Error checking for order status: {e}')

        if check[0]['status'] == 'open':
            print('Order placed at {}'.format(pd.Timestamp.now()))
            break
        else:
            print('Order was either filled or canceled at {}'.format(pd.Timestamp.now()))
            break


