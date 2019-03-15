'''
配合生成的K线数据，进行报单
1、与K线数据相同的成交价
2、配合生成深度报单
'''
import sys
sys.path.append('D:\\Robin\\UniDAX_NonObjectMM')

import time
import pandas as pd
import random

# 参数
_code = 'ethusdt'
_date = '2019-03-15'
_envo = 'Test'

# 导入参数
import Kline
# from Kline import Param as Kline_Param
CoinPARAM = Kline.Param.Run(_code, _envo)

# 设置交易环境
from Api.UniDax import UniDaxServices as uds
uds.Set(CoinPARAM['Basic']['Envo'])

# 设置交易接口
# from Kline import Trading as Kline_Trading

# 内部变量
struct_time = time.strptime(_date, "%Y-%m-%d")
TimeStamp = int(time.mktime(struct_time))
PricePrecision = int(CoinPARAM['Basic']['PricePrecision'])
VolumePrecision = int(CoinPARAM['Basic']['VolumePrecision'])
PriceTick = float(CoinPARAM['Basic']['PriceTick'])
VolumeTick = float(CoinPARAM['Basic']['VolumeTick'])
BidOrders = [] # 正在挂的买单
AskOrders = [] # 正在挂的卖单

# print('%s,%s,%s' %(PricePrecision, VolumePrecision, PriceTick))

'''
读取Excel
'''
path = 'D:\\Robin\\UniDAX_NonObjectMM\\Kline\\Trading\\'
path += '%s%s%s' %(struct_time.tm_year, struct_time.tm_mon,struct_time.tm_mday)
path += '\\%s.xlsx' %(_code)
df = pd.read_excel(path, index_col=0)
df = df.astype(float)

'''
开始前撤所有挂单
'''
Kline.Trading.cancel_all(_code)


'''
报单交易
'''
row_count = 0  # 操作到的行数
row_max = df.shape[0]# k线行数

# 循环：执行完最后一行退出
while row_count < row_max:

    nowTime = time.time()
    nextTime = df.loc[row_count, 'TimeStamp']
    Price = df.loc[row_count, 'ClosePrice']
    Price = round(Price, PricePrecision)
    Vol = df.loc[row_count, 'Vol']
    Vol = round(Vol, VolumePrecision)

    maxPrice = Price
    minPrice = Price

    OrderList = []

    '''
    计算报单
    '''
    if nowTime >= nextTime:

        # 加过滤，1分钟以前的就不做了
        if nowTime <= nextTime + 60:
            print('* 开始报单，now=%s，next=%s, spread=%s' %(nowTime, nextTime, nowTime-nextTime))

            # 生成报单：深度
            for i in range(3):
                # ask order
                r1 = random.randint(1, 3)  # 价格随机数，每两报单相隔 1-3跳
                r2 = random.uniform(0.2, 5)  # 数量随机数
                ap = maxPrice + r1 * PriceTick
                av = Vol * r2
                temp = {'price': ap, 'vol': av, 'dict': 'SELL'}
                OrderList.append(temp)
                maxPrice = ap

                # bid order
                r1 = random.randint(1, 3)  # 价格随机数，每两报单相隔 1-3跳
                r2 = random.uniform(0.2, 2)  # 数量随机数
                ap = minPrice - r1 * PriceTick
                av = Vol * r2
                temp = {'price': ap, 'vol': av, 'dict': 'BUY'}
                OrderList.append(temp)
                minPrice = ap

            # 生成报单：成交
            temp = {'price': Price, 'vol': Vol, 'dict': 'BUY'}
            OrderList.append(temp)
            temp = {'price': Price, 'vol': Vol, 'dict': 'SELL'}
            OrderList.append(temp)
            print('* p=%s, v=%s' %(Price, Vol))

            # 所有报单做精度处理
            for i in range(len(OrderList)):
                p = OrderList[i]['price']
                v = OrderList[i]['vol']

                OrderList[i]['price'] = round(p, PricePrecision)
                OrderList[i]['vol'] = round(v, VolumePrecision)

            '''
            把挡住成交价格的单子撤掉，剩余单子不动
            '''
            for ask in AskOrders:
                if Price > ask['price']:
                    Kline.Trading.cancel(_code, ask['id'])
                    AskOrders.remove(ask)

            for bid in BidOrders:
                if Price < bid['price']:
                    Kline.Trading.cancel(_code, bid['id'])
                    BidOrders.remove(bid)

            # 再随机撤一个单子
            askCount = len(AskOrders)
            bidCount = len(BidOrders)
            if askCount + bidCount > 0:
                r = random.randint(0, askCount + bidCount - 1)
                if r < askCount:
                    id = AskOrders[r]['id']
                    AskOrders.remove(AskOrders[r])
                else:
                    id = BidOrders[r-askCount]['id']
                    BidOrders.remove(BidOrders[r-askCount])

                Kline.Trading.cancel(_code, id)

            '''
            报新单
            '''
            for order in OrderList:
                p = order['price']
                v = order['vol']
                c = _code
                d = order['dict']
                re = Kline.Trading.do_order(code=c, price=p, vol=v, direction=d)
                #print(re)

                if re != 'Failed':
                    temp = {'id': re['data']['order_id'], 'price': p}
                    if d == 'SELL':
                        AskOrders.append(temp)
                    else:
                        BidOrders.append(temp)



            # #print(OrderList)
            # '''
            # 记录已有报单
            # '''
            # old_order = Core_Trading.get_all_order(_code)
            #
            # '''
            # 撤旧单
            # '''
            # Core_Trading.cancel(_code, old_order)



        # 行数进1
        row_count += 1
    else:
        time.sleep(1)
