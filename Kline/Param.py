'''
获取参数
'''
import pandas as pd
from pprint import *
import os


'''
读取参数
'''
def Run(_c, _e):
    # 各参数
    PARMA = {}
    # 读取环境参数
    df = pd.read_excel('D:\\Robin\\UniDAX_NonObjectMM\\Setting\\CoinParam.xlsx', header=2)
    #pprint(_envo)
    # 读取交易参数
    for i in range(df.shape[0]):
        if df.loc[i, 'Coin'] == _c and df.loc[i, 'Envo'] == _e:
            # 读取txt
            path = 'D:\\Robin\\UniDAX_NonObjectMM\\Setting\\%s\\%s.txt' % ( _e, _c)
            if not os.path.exists(path):
                w = open(path,'w')
                w.write('LastPrice=0\nLastVol=0\nBasePrice=0\nBaseVol=0')
            f = open(path)
            data = f.read().split('\n')

            # 构建参数
            PARMA = {'Basic':{}, 'Kline':{}, 'RealTime':{}, 'Trading':{}}

            # Basic信息
            PARMA['Basic']['Coin'] = _c
            PARMA['Basic']['Envo'] = _e
            t = float(df.loc[i, 'PricePrecision'])
            PARMA['Basic']['PriceTick'] = pow(10, -t)
            PARMA['Basic']['PricePrecision'] = t
            t = float(df.loc[i, 'VolumePrecision'])
            PARMA['Basic']['VolumeTick'] = pow(10, -t)
            PARMA['Basic']['VolumePrecision'] = t

    return PARMA

#pprint(Run('btcusdt','Test'))