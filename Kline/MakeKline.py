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

# 参与报价币种
_code = 'btcusdt'
_KlineDirectory = 'TestKline'
_Time = 'Now'
_price = 3000
_vol = 1

'''
内部参数
'''
isfirst = True
priceRatio = 0.0
volRatio = 0.0

beginTime = 0

'''
读取Excel
'''
directory_path = 'D:\\Robin\\UniDAX_NonObjectMM\\Kline\\%s' % (_KlineDirectory)
file_list = os.listdir(directory_path)

if _Time == 'Now':
    runTime = int(time.time())

for file in file_list:
    # 日内参数
    TradingDic = {}

    #
    df = pd.read_excel('%s\\%s' % (directory_path, file))
    df = df.sort_values(by='id')  # 按时间排序
    row_count = df.shape[0]
    if row_count != 1440:
        print('检查K线数据%s:并非分钟线' %(file))
        continue

    '''
    第一个K线进行定价
    '''
    if isfirst:
        cp = float(df.iloc[i,:].loc[:,'close'])
        at = float(df.iloc[i,:].loc[:,'amount'])
        priceRatio = _price / cp
        volRatio = _vol / at
        isfirst = False

    '''
    根据指定参数进行处理
    '''
    for i in range(row_count):
        ClosePrice = float(df.iloc[i,:].loc[:,'close'])
        High = float(df.iloc[i,:].loc[:,'high'])
        Low = float(df.iloc[i, :].loc[:, 'low'])

        # 1分钟内，做3个成交，对应最高、最低和收盘
        sumSecond = 0
        priceList = [ClosePrice, High, Low]

        for i in range(3):
            # 时间
            r = random.randint(i , 60 - sumSecond)
            sumSecond = r

            #
            r = random.randint(0, len(priceList) - 1)
            runPrice = priceList[r] * priceRatio

        # 结束本分钟计算，进1分钟
        runTime += 60



    pprint(df)
#     for i in range(row_count):
#
#         # 取个随机
#         r = int(random.uniform(each_turn * 0.6, each_turn * 1.4))
#
#
#
# pprint(file_list)
