'''
通过成交价信息，生成报单
1、自成交报单
2、深度报单
'''
import random

def Run(coinParam):
    # 格式化一下
    _tp = float(coinParam['Trading']['LastPrice'])
    _tv = float(coinParam['Trading']['LastVol'])
    _pt = float(coinParam['Info']['PriceTick'])
    _vt = float(coinParam['Info']['VolumeTick'])
    _envo = coinParam['Envo']

    # 自成交报单
    # 加个随机波动吧
    OrdeList = []
    r = random.randint(-3,3)
    orderprice = _tp + r * _pt
    temp = {'price': orderprice, 'vol': _tv, 'dict': 'BUY', 'envo':_envo}
    OrdeList.append(temp)
    temp = {'price': orderprice, 'vol': _tv, 'dict': 'SELL', 'envo':_envo}
    OrdeList.append(temp)

    # 深度报单
    maxPrice = _tp
    minPrice = _tp

    # 前10报单 较密集
    for i in range(10):
        # ask order
        r1 = random.randint(1, 3) # 价格随机数，每两报单相隔 1-3跳
        r2 = random.uniform(0.2, 2) # 数量随机数
        ap = maxPrice + r1 * _pt
        av = (OrdeList[0]['vol'] + OrdeList[-1]['vol']) * r2
        temp = {'price': ap, 'vol': av, 'dict': 'SELL', 'envo':_envo}
        OrdeList.append(temp)
        maxPrice = ap

        # bid order
        r1 = random.randint(1, 3)  # 价格随机数，每两报单相隔 1-3跳
        r2 = random.uniform(0.2, 2)  # 数量随机数
        ap = minPrice - r1 * _pt
        av = (OrdeList[0]['vol'] + OrdeList[-1]['vol']) * r2
        temp = {'price': ap, 'vol': av, 'dict': 'BUY', 'envo':_envo}
        OrdeList.append(temp)
        minPrice = ap

    # 后5报单，较松散
    for i in range(5):
        # ask order
        r1 = random.randint(3, 10)  # 价格随机数，每两报单相隔 1-3跳
        r2 = random.uniform(0.2, 1.5)  # 数量随机数
        ap = maxPrice + r1 * _pt
        av = (OrdeList[0]['vol'] + OrdeList[-1]['vol']) * r2
        temp = {'price': ap, 'vol': av, 'dict': 'SELL', 'envo':_envo}
        OrdeList.append(temp)
        maxPrice = ap

        # bid order
        r1 = random.randint(3, 10) # 价格随机数，每两报单相隔 1-3跳
        r2 = random.uniform(0.2, 1.5)  # 数量随机数
        ap = minPrice - r1 * _pt
        av = (OrdeList[0]['vol'] + OrdeList[-1]['vol']) * r2
        temp = {'price': ap, 'vol': av, 'dict': 'BUY', 'envo':_envo}
        OrdeList.append(temp)
        minPrice = ap

    '''
    对价格做精度处理
    '''
    for order in OrdeList:
        _price = float(order['price'])
        _vol = float(order['vol'])
        _pp = int(coinParam['Info']['PricePrecision'])
        _vp = int(coinParam['Info']['VolumePrecision'])

        _new_price = round(_price, _pp)
        _new_vol = round(_vol, _vp)


        # 如果是整数，那么把数据类型改为int
        if _price == int(_price):
            order['price'] = int(_new_price)
        else:
            order['price'] = _new_price

        if _vol == int(_vol):
            order['vol'] = int(_new_vol)
        else:
            order['vol'] = _new_vol


    return OrdeList