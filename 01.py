import pyupbit
import time
import datetime

from pyupbit.exchange_api import Upbit 

def cal_target(ticker):
    df = pyupbit.get_ohlcv(ticker, "day")
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high']-yesterday['low']
    target = today['open'] + yesterday_range * 0.3
    return target

# 객체 생성
access = "access-key"
secret = "secret-key"
upbit = pyupbit.Upbit(access, secret)

# 변수 설정
target = cal_target("KRW-ETH")
op_mode = False
hold = False

while True:
    now = datetime.datetime.now()

    # 매도 시도
    if now.hour == 8 and now.minute == 59 and 50 <= now.second <= 59:
        if op_mode is True and hold is True:
            btc_balance = upbit.get_balance("KRW-ETH")
            upbit.sell_market_order("KRW-ETH", btc_balance)
            hold = False
        op_mode = False
        time.sleep(10)

    # 09:00:00 목표가 갱신
    if now.hour == 9 and now.minute == 0 and 20 <= now.second <=30:
        target = cal_target("KRW-ETH")
        op_mode = True

    price = pyupbit.get_current_price("KRW-ETH")
    
    # 매초마다 조건을 확인한 후 매수 시도
    if op_mode is True and price is not None and hold is False and price >= target:
        # 매수
        krw_balance = upbit.get_balance("KRW")
        upbit.buy_market_order("KRW-ETH", krw_balance*0.9995)
        hold = True
    
    # 상태출력
    print(f"현재시간: {now} 목표가: {target} 현재가: {price} 보유상태: {hold} 동작상태: {op_mode}")

    time.sleep(1)
