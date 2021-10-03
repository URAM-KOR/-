import win32com.client
import pandas as pd

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음.  ")
    exit()


# 전체 종목정보 가져오기

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
codeList = instCpCodeMgr.GetStockListByMarket(1)
rows = []
CPE_MARKET_KIND = {'KOSPI':1, 'KOSDAQ':2}

for key, value in CPE_MARKET_KIND.items():
    codeList = instCpCodeMgr.GetStockListByMarket(value)
    for code in codeList:
        name = instCpCodeMgr.CodeToName(code)
        sectionCode = instCpCodeMgr.GetStockSectionKind(code)
        rows.append([code, sectionCode, name, key])

stockitems = pd.DataFrame(data= rows, columns=['code','sectionKind','name','section'])
stockitems.loc[stockitems['sectionKind'] == 10, 'section'] = 'ETF'
stockitems = stockitems.drop('sectionKind',axis=1)
print(stockitems)
stockitems.to_csv('stockitems.csv', index=False)