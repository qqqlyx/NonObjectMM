'''
获取实时数据：火币
按照参数进行修改
输出：目标成交价
'''

# 币种参数
Coin = ''  # 币种
PriceRange = [] # 价格范围

# 标的物参数
TargetBasket = {}


# test
Coin = 'btcusdt'
PriceRange = [3700, 3800]
TargetBasket = {'ethusdt':0.5, 'btcusdt':0.5}

# 获取火币实时数据

