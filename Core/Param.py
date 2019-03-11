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
            # Basic信息
            #PARMA['Coin'] = _c
            #PARMA['Envo'] = _e
            PARMA['Basic']['Coin'] = _c
            PARMA['Basic']['Envo'] = _e
            t = float(df.loc[i, 'PricePrecision'])
            PARMA['Basic']['PriceTick'] = pow(10, -t)
            PARMA['Basic']['PricePrecision'] = t
            t = float(df.loc[i, 'VolumePrecision'])
            PARMA['Basic']['VolumeTick'] = pow(10, -t)
            PARMA['Basic']['VolumePrecision'] = t

            # Kline信息
            PARMA['Kline']['EachKlineDay'] = df.loc[i, 'EachKlineDay']
            PARMA['Kline']['KlineDirectory'] = df.loc[i, 'KlineDirectory']

            # RealTime信息
            PARMA['RealTime']['PriceUp'] = float(df.loc[i, 'PriceUp'])
            PARMA['RealTime']['PriceLow'] = float(df.loc[i, 'PriceLow'])
            temp = {}
            for x in range(5):
                t = x + 1
                bname = 'TargetBasket%s' % (t)
                vname = 'ratio%s' % (t)
                b = df.loc[i, bname]
                v = df.loc[i, vname]
                if b == b and v == v:  # b和v都不是NaN
                    temp[b] = v
            PARMA['RealTime']['Basket'] = temp

            # 交易参数 Trading
            PARMA['Trading']['LastPrice'] = float(data[0].split('=')[1])
            PARMA['Trading']['LastVol'] = float(data[1].split('=')[1])
            PARMA['Trading']['BasePrice'] = float(data[2].split('=')[1])
            PARMA['Trading']['BaseVol'] = float(data[3].split('=')[1])


    '''
    交易参数，进行首次定价
    '''
    t = PARMA['Trading']
    if t['LastPrice'] <= 0 or t['LastVol'] <= 0:
        # 初次交易
         print('请进行定价！')

    return PARMA

#pprint(Run('btcusdt','Test'))