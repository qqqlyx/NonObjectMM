from Api.Huobi import HuobiServices as hbs
from Api.UniDax import UniDaxServices as uds
import pandas as pd
from pprint import *
import time
import datetime
import random
import math
from Api.UniDax import Tokens
from RealTime import *
from Kline import *
from Core import Trading as Core_Trading

import sys
sys.path.append('D:\\Robin\\UniDAX_NonObjectMM')

price = 152.41
tick = 0.01
direction = 1
uds.Set('Test')

old_order = Core_Trading.get_all_order('ethusdt')
Core_Trading.cancel('ethusdt', old_order)

while True:

    direction *= -1

    for i in range(random.randint(10,50)):
        r = random.randint(1,5)
        price += r * tick * direction
        vol = random.uniform(0.001, 10.000)
        vol = round(vol, 3)
        uds.create_order(symbol='ethusdt', side='BUY', volume=vol, price=price)
        uds.create_order(symbol='ethusdt', side='SELL', volume=vol, price=price)

        time.sleep(0.1)

