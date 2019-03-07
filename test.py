from Api.Huobi import HuobiServices as hbs
from Api.UniDax import UniDaxServices as uds
import pandas as pd
from pprint import *
import time
import datetime
import random
import math
from Api.UniDax import Tokens
from Core import *

# # 记录各类常数
# stock_list = []
# f = open('D:\\Robin\\UniDAX_NSMM\\Setting\\coin_list.txt')
# data = f.read()
# d = data.split('\n')
#
# envo = d[0].split('=')[1].replace(' ', '')
#
# S = d[1].split('=')[1]
# S2 = S.split(',')
# for s in S2:
#     stock_list.append(s.replace(' ', ''))
#
# df = pd.DataFrame(index = stock_list, columns=['Price','Volume'])
# v1 = []
# p1 = []
# for coin in stock_list:
#     v = Constant.get_precision(coin,'volume')
#     p = Constant.get_precision(coin,'price')
#     v1.append(v)
#     p1.append(p)
#
# df['Price'] = p1
# df['Volume'] = v1
# df.to_excel('D:\\Robin\\UniDAX_NSMM\\Setting\\test.xlsx')

# t = hbs.get_kline('btcusdt', '1min',size=10)
# df = pd.DataFrame(t['data'])
# new_df = df.loc[df['id'] >= 1551346200]
# #new_df = new_df.loc[new_df['id'] <= 1551346200]
# new_df.to_excel('')
# print(new_df)
# df.to_excel(index\
#             )

# a = int(time.time())
# tss1 = '%s-%s-%s 00:00:00' %()
# print(a)
#
# t = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
# print(t)
# data = range(100)
# l = []
# for i in range(100):
#     i = i + 1
#     k = math.log(float(i))
#     l.append(k)
# print(l)

# t = math.atan(1)
# print(t)

# Tokens.set('Test')
# print(Tokens.UniDAX_APIKEY)
uds.Set('Test')
t = Trading.get_all_order('gntusdt')
#pprint(t)
Trading.cancel('gntusdt', t)
#uds.cancel_order('btcusdt', 70861)

t = uds.create_order('ethbtc',price= 5.124, volume= 20.5, side= 'SELL')