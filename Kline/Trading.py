import time
import json
from Api.UniDax import UniDaxServices as uds
from pprint import *

# 实际下单，返回信息
def do_order(code, price, vol, direction):
    result = 'Failed'

    try:
        time.sleep(0.01)
        #print('%s,%s,%s,%s' %(code, direction,price,vol))
        r = uds.create_order(symbol=code, side=direction, price=price, volume=vol)
        re = json.loads(r)  # 使用eval会报错，因次用了json方法转换str -> dict
        #print(re)
        # 打印log
        if re['msg'] != 'suc':
            #print('%s CODE=%s  D=%s  P=%s  V=%s' % (re, code, direction, price, vol))
            result = 'Failed'

        else:
            # log.info(re)
            result = re

    except Exception as e:
        print('---->except<do_trading>: ' + str(code), e)
        pass

    return result

# 撤单
def cancel(coin, order_id):
    id = str(order_id)
    r = uds.cancel_order(coin, id)
    re = json.loads(r)  # 使用eval会报错，因次用了json方法转换str -> dict
    # 打印log
    if re['msg'] != 'suc':
        pass
        # print('(cancel_all): code: ' + code)
        # print(re)
    # else:
    #     log.info(re)

    return

# 撤全部
def cancel_all(coin):
    orders = uds.new_order(coin)
    if orders['data']['count'] > 0:
        for data in orders['data']['resultList']:
            id = data['id']
            uds.cancel_order(coin, id)
    return

#
# # 获取全部订单
# def get_all_order_id(coin):
#     orders = uds.new_order(coin)
#
#         # # 打印log
#         # if orders['msg'] != 'suc':
#         #     log.error(orders)
#         # else:
#         #     log.info(orders)
#
#     return orders
#
# uds.Set('Test')
# t = get_all_order_id('ethusdt')
# pprint(t)