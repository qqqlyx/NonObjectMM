'''
0、读取参数
循环：
1、计算出下单价格
2、生成成交报单
3、依据成交价格，填充报单队列
4、下单交易
'''

# 设定报单币种
# COIN = 'btcusdt'
# ENVO = 'Test' # Official
# DATA = 'RealTime'  # Kline

import sys
sys.path.append('D:\\Robin\\UniDAX_NonObjectMM')

_input_param = str(sys.argv[1]).split(',')
COIN = _input_param[0]
ENVO = _input_param[1]
DATA = _input_param[2]
print('%s,%s,%s' %(COIN,ENVO,DATA))
#print('*%s' %(sys.argv[1]))

# 交易参数
mm_fre = 15 # 交易周期 秒
write_fre = 10 # 交易数据备份周期 分钟

# 读取参数
import Core
CoinPARAM = Core.Param.Run(COIN, ENVO)

# 设置交易环境
from Api.UniDax import UniDaxServices as uds
uds.Set(CoinPARAM['Basic']['Envo'])

# 导入数据模块
from RealTime import Huobi as RealTime_Huobi
#from Kline import

if DATA == 'RealTime':
    DataFunction = RealTime_Huobi
# elif DATA == 'Kline':
#     DataFunction = Kline.GetData


# 导入其他模块
import time

# 定时参数
write_param_stamp = time.time()
mm_stamp = time.time()

#pprint(Tokens.UniDAX_unidax_url)

#
time_tick = 0

# 开始报单循环
while True:
    '''
    构建报单列表
    '''
    # 变量
    order_list = []

    time_tick = int(time.time())

    # 计算下单价格
    CoinPARAM['Trading'] = DataFunction.Run(CoinPARAM)

    ts = int(time.time() - time_tick)
    print('* 计算价格 时间 = %s ' %(ts))
    time_tick = int(time.time())

    # 生成报单信息
    Order_List = Core.get_OrderList.Run(CoinPARAM)

    ts = int(time.time() - time_tick)
    print('* Order_List 时间 = %s ' % (ts))

    '''
    交易下单
    '''
    time_tick = int(time.time())
    # 先记录所有单号，接着进行报单，最后再撤上一批报单
    all_order = Core.Trading.get_all_order(COIN)
    ts = int(time.time() - time_tick)
    print('* all_order 时间 = %s ' % (ts))


    # 进行报单
    time_tick = int(time.time())
    for order in Order_List:
        p = order['price']
        v = order['vol']
        c = COIN
        d = order['dict']
        Core.Trading.do_order(code=c, price=p, vol=v, direction=d)
    ts = int(time.time() - time_tick)
    print('* 报单 时间 = %s ' % (ts))


    # 撤上一批次报单
    time_tick = int(time.time())
    Core.Trading.cancel(COIN, all_order)
    ts = int(time.time() - time_tick)
    print('* 撤单 时间 = %s ' % (ts))


    '''
    记录交易信息, 10分钟备份一次
    '''
    if time.time() - write_param_stamp >= (write_fre * 60):
        write_param_stamp = time.time()

        # 记录交易参数
        _e = CoinPARAM['Basic']['Envo']
        _c = CoinPARAM['Basic']['Coin']
        path = 'D:\\Robin\\UniDAX_NonObjectMM\\Setting\\%s\\%s.txt' % (_e, _c)

        lp = str(CoinPARAM['Trading']['LastPrice'])
        lv = str(CoinPARAM['Trading']['LastVol'])
        bp = str(CoinPARAM['Trading']['BasePrice'])
        bv = str(CoinPARAM['Trading']['BaseVol'])

        w = open(path, 'w')
        w.write('LastPrice=%s\nLastVol=%s\nBasePrice=%s\nBaseVol=%s' % (lp, lv, bp, bv))
        w.close()


    '''
    根据交易周期进行休眠
    '''
    trading_time = time.time() - mm_stamp # 交易流程运行时间
    mm_stamp = time.time() # 赋值
    print('* 运行时间=%s' %(str(trading_time)))
    sleep_time = mm_fre - trading_time # 计算睡眠时间
    if sleep_time > 0:
        time.sleep(mm_fre)




