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

# # 参与报价币种
# _code = sys.argv[1]
# _KlineDirectory = sys.argv[2]
# _Time = sys.argv[3]  # Now / NextDay
# _price = sys.argv[4]  # 初始定价价格
# _vol = sys.argv[5]  # 初始定量
#
# '''
# 读取Excel
# '''
# directory_path = 'D:\\Robin\\UniDAX_NonObjectMM\\Run\\%s' % (_KlineDirectory)
# file_list = os.listdir(directory_path)
#
# for file in file_list:
#     df = pd.read_excel('%s\\%s' % (directory_path, file))
#
#     '''
#     根据指定参数进行处理
#     '''
#     row_count = df.shape[0]
#     if row_count != 1440:
#         print('检查K线数据%s:并非分钟线' %(file))
#
#     total_seconds = 86400  # 需要把K线分布在1天内
#     each_turn = total_seconds // row_count
#
#     for i in range(row_count):
#
#         # 取个随机
#         r = int(random.uniform(each_turn * 0.6, each_turn * 1.4))
#
#
#
# pprint(file_list)
