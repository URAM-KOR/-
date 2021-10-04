import win32com.client
import pandas as pd
import datetime

instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

#데이터 구성
instStockChart.SetInputValue(0, "A003540")
instStockChart.SetInputValue(1, ord('2'))
instStockChart.SetInputValue(4, 200)
instStockChart.SetInputValue(5, (0,1,2,3,4,5,6,8,9))
instStockChart.SetInputValue(6, ord('m'))
instStockChart.SetInputValue(7, 15)
instStockChart.SetInputValue(9, ord('1'))

datacolumn = ['Date', 'Open', 'High','Low', 'Close',
              'Change','Volume']
data = []

#데이터 요청
instStockChart.BlockRequest()

numData = instStockChart.GetHeaderValue(3)

for i in range(numData):
    data.append([str(instStockChart.GetDataValue(0, i))+str(instStockChart.GetDataValue(1, i)),
    instStockChart.GetDataValue(2, i),
    instStockChart.GetDataValue(3, i),
    instStockChart.GetDataValue(4, i),
    instStockChart.GetDataValue(5, i),
    instStockChart.GetDataValue(6, i),
    instStockChart.GetDataValue(8, i)])

stockdata = pd.DataFrame(data= data, columns=datacolumn)
stockdata['Date']=pd.to_datetime(stockdata['Date'],format='%Y%m%d%H%M')
print(stockdata)
stockdata.to_csv('stockdata.csv', index=False)