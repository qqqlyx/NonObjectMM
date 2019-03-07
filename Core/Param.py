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
    df = pd.read_excel('D:\\Robin\\UniDAX_NSMM\\Setting\\CoinParam.xlsx')
    #pprint(_envo)
    # 读取交易参数
    for i in range(df.shape[0]):
        if df.loc[i, 'Coin'] == _c or df.loc[i, 'Envo'] == _e:
            # 读取txt
            path = 'D:\\Robin\\UniDAX_NSMM\\Setting\\%s\\%s.txt' % ( _e, _c)
            if not os.path.exists(path):
                w = open(path,'w')
                w.write('LastPrice=0\nLastVol=0\nBasePrice=0\nBaseVol=0')
            f = open(path)
            data = f.read().split('\n')
            # 代码
            PARMA['Coin'] = _c
            PARMA['Envo'] = _e
            # 交易参数 Trading
            temp = {}
            temp['LastPrice'] = float(data[0].split('=')[1])
            temp['LastVol'] = float(data[1].split('=')[1])
            temp['BasePrice'] = float(data[2].split('=')[1])
            temp['BaseVol'] = float(data[3].split('=')[1])
            PARMA['Trading'] = temp
            # 币种参数 Coin
            temp = {}
            t = float(df.loc[i, 'PricePrecision'])
            temp['PriceTick'] = pow(10,-t)
            temp['PricePrecision'] = t
            t = float(df.loc[i, 'VolumePrecision'])
            temp['VolumeTick'] = pow(10, -t)
            temp['VolumePrecision'] = t
            temp['PriceUp'] = float(df.loc[i, 'PriceUp'])
            temp['PriceLow'] = float(df.loc[i, 'PriceLow'])
            PARMA['Info'] = temp
            # 标的篮子参数 Basket
            temp = {}
            for x in range(5):
                t = x + 1
                bname = 'TargetBasket%s' %(t)
                vname = 'ratio%s' %(t)
                b = df.loc[i, bname]
                v = df.loc[i, vname]
                if b == b and v == v: # b和v都不是NaN
                    temp[b] = v
            PARMA['Basket'] = temp



    '''
    交易参数，进行首次定价
    '''
    t = PARMA['Trading']
    if t['LastPrice'] <= 0 or t['LastVol'] <= 0:
        # 初次交易
         print('请进行定价！')

    return PARMA

#pprint(Run('btcusdt','Test'))