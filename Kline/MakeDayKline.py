'''
通过K线数据进行报价
K线数据，必须是分钟线
会做出6-8个成交，满足收盘、最高、最低价格

输入：上次报价（作为K线初始价格）
输入：定价范围
输出：价格和数量
'''

import pandas as pd
from pprint import *
import time
import datetime
import math
import os
import sys
import random

# 参与报价币种
# _code = sys.argv[1]
# _KlineDirectory = sys.argv[2]
# _Time = sys.argv[3]  # Now / NextDay
# _price = sys.argv[4]  # 初始定价价格
# _vol = sys.argv[5]  # 初始定量

# 参数
_code = 'ltcusdt'
_kline = 'TestKline\\kline_1.xlsx'
_date = '2019-03-15'
_begin_price = 15
_begin_vol = 1

'''
内部参数
'''
priceRatio = 0.0
volRatio = 0.0
BeginStamp = int(time.mktime(time.strptime(_date, "%Y-%m-%d")))  # 当日TimeStamp
runTime = BeginStamp

'''
读取Excel, 对应火币分钟线数据
'''
path = 'D:\\Robin\\UniDAX_NonObjectMM\\Kline\\%s' % (_kline)
df = pd.read_excel(path)

# 处理数据格式
df = df.astype(float)
df = df.sort_values(by='id')  # 按时间排序

# 检查数量
if df.shape[0] != 1440:
    print('请检查K线数据, [%s]并非分钟线' % (_kline))


'''
根据第一个开盘价进行定价
'''
op = df.iloc[0, :]['open']
vol = df.iloc[0, :]['amount']
priceRatio = _begin_price / op
volRatio = _begin_vol / vol


'''
根据参数进行处理
'''
DayPrice = []
DayTime = []
DayVol = []

for i in range(df.shape[0]):
    ClosePrice = float(df.iloc[i, :]['close'])
    High = float(df.iloc[i, :]['high'])
    Low = float(df.iloc[i, :]['low'])
    Vol = float(df.iloc[i,:]['amount'])

    #
    # 生成报单数量和价格
    #
    OrderList = []

    # 做0-3个成交，价格处于最高和最低中间
    # 不做了，随机成交情况由单独程序控制
    # r = random.randint(0, 3)
    # for j in range(r):
    #     p = random.uniform(Low, High)
    #     OrderList.append(p)

    # 把最高价和最低价插入，并把列表顺序打乱
    OrderList.append(High * priceRatio)
    OrderList.append(Low* priceRatio)
    random.shuffle(OrderList)

    # 最后插入收盘价
    OrderList.append(ClosePrice * priceRatio)

    #
    # 成交量
    #
    OrderVol = []
    count = len(OrderList)

    meanVol = Vol / count
    for j in range(count):
        min = j * meanVol
        max = (j + 1) * meanVol
        vol = random.uniform(min, max)
        final = vol * volRatio
        OrderVol.append(final)


    #
    # 生成报单时间，每个成交之间，至少相隔5秒
    #
    OrderTime = []

    meanTime = 60 / count
    for j in range(count):
        min = j * meanTime
        max = (j + 1) * meanTime
        rtime = random.uniform(min, max)
        final = int(runTime + rtime)
        OrderTime.append(final)

    # 结束本分钟计算，进1分钟
    runTime += 60

    #
    # 保存
    #
    DayPrice += OrderList
    DayTime += OrderTime
    DayVol += OrderVol

'''
写Excel
'''

# 加一点随机

for j in range(len(DayPrice)):
    r = random.uniform(0.9999, 1.0001)
    p = DayPrice[j]
    DayPrice[j] = p * r


dict = {'TimeStamp':DayTime, 'ClosePrice':DayPrice, 'Vol':DayVol}
newDF = pd.DataFrame(dict)

date = time.localtime(BeginStamp)

path = 'D:\\Robin\\UniDAX_NonObjectMM\\Kline\\Trading\\'
path += '%s%s%s' %(date.tm_year, date.tm_mon,date.tm_mday)

if not os.path.exists(path):
      os.makedirs(path)

path += '\\%s.xlsx' %(_code)
newDF.to_excel(path)

