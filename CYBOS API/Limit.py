import win32com.client
import time


nCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
nCpCybos.GetLimitRemainCount(1) # 0: 주문관련 요청 / 1: 시세조회관련 요청


for idx, stockitem in stockitems.iterrows():
    remain_request_count = nCpCybos.GetLimitRemainCount(1)
    print(stockitem['code'], stockitem['name'], '남은 요청 : ', remain_request_count)
    if remain_request_count == 0:
        print('남은 요청이 모두 소진되었습니다. 잠시 대기합니다.')
        while True:
            time.sleep(2)
            remain_request_count = nCpCybos.GetLimitRemainCount(1)
            if remain_request_count > 0:
                print('작업을 재개합니다. (남은 요청 : {0})'.format(remain_request_count))
                break
            print('대기 중...')