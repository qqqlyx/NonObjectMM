'''
获取实时数据：火币
根据基准价格BasePrice的涨跌，计算最新成交价格

输入：上次报价
输入：定价范围
输出：价格和数量的涨跌幅
'''

from Api.Huobi import HuobiServices as hbs
from Api.UniDax import UniDaxServices as uds
import pandas as pd
from pprint import *
import time
import datetime
import math

# # 输入参数
# LastPrice = 0 # 上次报价
# LastVol = 0 # 上次数量
# PriceUp = 0 # 定价范围
# PriceLow = 0
# TargetBasket = {} # 标的篮子，币种和权重
#
# # 基准数据
# BasePrice = 0
# BaseVol = 0
#
# # test
# PriceUp = 3800
# PriceLow = 3700
# LastPrice = 3740
# LastVol = 3
# TargetBasket = {'ethusdt':0.5, 'btcusdt':0.5}
# BasePrice = 1981.55
# BaseVol = 1.2


def Run(coinParam):
    '''
    通过实时行情计算最新成交价，并使用反正切函数进行处理
    :param coinParam: 统一参数
    :return:
    '''
    _targetBasket = coinParam['RealTime']['Basket']
    _lastPrice = coinParam['Trading']['LastPrice']
    _lastVol = coinParam['Trading']['LastVol']
    _basePrice = coinParam['Trading']['BasePrice']
    _baseVol = coinParam['Trading']['BaseVol']
    _priceUp = coinParam['RealTime']['PriceUp']
    _priceLow = coinParam['RealTime']['PriceLow']

    #print('1* %s%s%s%s' %(_lastPrice,_lastVol,_basePrice,_baseVol))

    # 获取火币实时数据
    # (ask + bid)/ 2
    # 价格 和 量
    _huobiQuota = {}
    for key in _targetBasket.keys():
        t = hbs.get_depth(symbol=key, type='step0')
        p = (t['tick']['asks'][0][0] + t['tick']['bids'][0][0]) / 2
        v = (t['tick']['asks'][0][1] + t['tick']['bids'][0][1]) / 2

        _huobiQuota[key] = {'Price': p, 'Vol': v}


    # 按权重，计算新基准价
    # 计算新基准量
    _newBase = 0
    _newBaseVol = 0
    for key in _targetBasket.keys():
        r = float(_targetBasket[key])
        p = float(_huobiQuota[key]['Price'])
        v = float(_huobiQuota[key]['Vol'])
        _newBase += p * r
        _newBaseVol += v * r


    '''
    首次定价，以当前
    '''
    if _basePrice <= 0 or _baseVol <= 0:
        # 返回结果
        #print('*')
        result = {'LastPrice': _lastPrice, 'LastVol': _lastVol, 'BasePrice': _newBase, 'BaseVol': _newBaseVol}
    else:
        # 计算涨跌幅度
        #print('*****')
        _ratioP = (_newBase - _basePrice) / _basePrice
        _ratioV = (_newBaseVol - _baseVol) / _baseVol
        #print('2* %s%s' % (_ratioP, _ratioV))
        #print('base_ratio=%s' % (_ratioP * 100))

        # 根据价格范围 调整价格涨跌
        # 使用反正切函数控制
        NewPrice = _lastPrice * (1 + _ratioP)
        #print('price=%s' % (NewPrice))

        #NewPrice = get_final_price_atan(_priceUp, _priceLow, NewPrice)

        # print(
        #     '_basePrice=%s, _newBase=%s, _lastPrice=%s, after_price=%s' % (_basePrice, _newBase, _lastPrice, NewPrice))

        br = round(_newBase / _basePrice,4)
        pr = round(NewPrice / _lastPrice, 4)
        print('baseRatio = %s, priceRatio = %s' %(br, pr))
        NewVol = _lastVol * (1 + _ratioV)




        # 返回结果
        result = {'LastPrice': NewPrice, 'LastVol': NewVol, 'BasePrice': _newBase, 'BaseVol': _newBaseVol}


    return result


# 根据价格范围 调整价格涨跌
# 使用反正切函数控制
# x = 新价格 - 均价
# y = 最终价格 - 均价
def get_final_price_atan(price_up, price_low, price):
    meanprice = (price_up + price_low) / 2
    spread = price_up - meanprice
    price_spread = abs(price - meanprice)

    print('price_spread=%s' %(price_spread))

    # 对于反正切函数来说,当x=1时, y=0.7853,大约是极限的1/2
    # y 的极限是 pi / 2
    x_ratio = 1 / (spread / 2) # x倍数
    y_ratio = spread / (math.pi / 2) # y倍数

    # 此处希望实现，当price_spread = 1/2 spread时，x=1
    x = price_spread * x_ratio
    y = math.atan(x)

    # 再计算回原始价差
    if price < meanprice:
        final_spread = -abs(y * y_ratio)
    else:
        final_spread = abs(y * y_ratio)

    print('final_spread=%s' % (final_spread))

    # 最终价格
    final_price = final_spread + meanprice

    return final_price

# list1 = []
# list2 = []
# for i in range(1000):
#     t = get_final_price_atan(3700, 3600, 3100 + i)
#     list1.append(t)
#     t = math.atan((i - 500) / 12.5)
#     list2.append(t)
# df = pd.Series(list1)
# df.to_excel('D:\\Robin\\UniDAX_NonObjectMM\\Setting\\Test\\test.xlsx')
# df = pd.Series(list2)
# df.to_excel('D:\\Robin\\UniDAX_NonObjectMM\\Setting\\Test\\test2.xlsx')

