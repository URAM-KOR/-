import time
import hmac
from requests import Request

YOUR_API_SECRET = 'QUsJaE8upSSdP9Rve1DRPEeGdcMMEUP-f2iIXiAO'
YOUR_API_KEY = 'VYXBrkmuhutN9cr2APKbblqW4esKX-0Euhe9evr4'


ts = int(time.time() * 1000)
request = Request('GET', 'https://ftx.com/markets')
prepared = request.prepare()
signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
signature = hmac.new(YOUR_API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

request.headers['FTX-KEY'] = YOUR_API_KEY
request.headers['FTX-SIGN'] = signature
request.headers['FTX-TS'] = str(ts)

# Only include line if you want to access a subaccount. Remember to URI-encode the subaccount name if it contains special characters!
request.headers['FTX-SUBACCOUNT'] = 'bot'
