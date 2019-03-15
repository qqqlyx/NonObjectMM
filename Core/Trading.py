import time
import json
from Api.UniDax import UniDaxServices as uds


# 实际下单，返回信息
def do_order(code, price, vol, direction):
    result = '000'

    try:
        time.sleep(0.01)
        r = uds.create_order(code, direction, price, vol)
        re = json.loads(r)  # 使用eval会报错，因次用了json方法转换str -> dict

        # 打印log
        if re['msg'] != 'suc':
            #print('%s CODE=%s  D=%s  P=%s  V=%s' % (re, code, direction, price, vol))
            result = '000'

        else:
            # log.info(re)
            result = re

    except Exception as e:
        pass
        # print('---->except<do_trading>: ' + str(code), e)

    return result

# 撤掉UniDAX全部挂单
def cancel(code, all_order):
    # 如果报单的key中有该代码，则进入撤单
    if all_order['data']['count'] > 0:
        for order in all_order['data']['resultList']:
            # if order['status'] == 1:
            id = str(order['id'])
            r = uds.cancel_order(code, id)
            re = json.loads(r)  # 使用eval会报错，因次用了json方法转换str -> dict
            # 打印log
            if re['msg'] != 'suc':
                pass
                # print('(cancel_all): code: ' + code)
                # print(re)
            # else:
            #     log.info(re)

    return

# 获取全部订单
def get_all_order(coin):
    orders = uds.new_order(coin)
        # # 打印log
        # if orders['msg'] != 'suc':
        #     log.error(orders)
        # else:
        #     log.info(orders)

    return orders