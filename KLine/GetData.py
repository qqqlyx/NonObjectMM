'''
通过K线数据进行报价

输入：上次报价（作为K线初始价格）
输入：定价范围
输出：价格和数量
'''

import pandas as pd
from pprint import *
import time
import datetime
import math

# coinParam = ''
# _each_kline_day = coinParam['']
#
# path = 'D:\\Robin\\UniDAX_NonObjectMM\\KLine\\'
#
#
# #def Run(coinParam):
# '''
# 读取Excel，并根据指定时间进行处理
# '''
# df = pd.read_excel(path)
#
# pprint(df)
#
#
# #Run()
