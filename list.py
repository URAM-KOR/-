import win32com.client

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
# codeList = instCpCodeMgr.GetStockListByMarket(1)
#
# for i, code in enumerate(codeList):
#     secondCode = instCpCodeMgr.GetStockSectionKind(code)
#     name = instCpCodeMgr.CodeToName(code)
#     print(i, code, secondCode, name)

