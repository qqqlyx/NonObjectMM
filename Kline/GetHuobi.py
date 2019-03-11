'''
定期获取火币K线数据
分钟
'''

from Api.Huobi import HuobiServices as hbs
from Core import Param
import pandas as pd

CoinList = set(Param.COIN['Coin'])
for coin in CoinList:
    t = hbs.get_kline(coin, '1min', size=2000)
    df = pd.DataFrame(t['data'])





