
import sys
sys.path.append('D:\\Robin\\UniDAX_NonObjectMM')

import datetime
from Api.Huobi import HuobiServices as hbs
import pandas as pd
import time

# 获取数据
# 读取环境参数
df = pd.read_excel('D:\\Robin\\UniDAX_NonObjectMM\\Setting\\CoinParam.xlsx')
CoinList = set(list(df.loc[:,'Coin']))


# 程序运行后，第二天零点开始导出数据
run_day = datetime.datetime.now() + datetime.timedelta(days=1)
tss1 = '%s-%s-%s 00:00:00' % (run_day.year, run_day.month, run_day.day)
timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
run_Stamp = int(time.mktime(timeArray))


while True:
    '''
    定期触发
    '''
    nowStamp = int(time.time())
    if nowStamp >= run_Stamp:
        lastStamp = run_Stamp - 86400

        for coin in CoinList:
            t = hbs.get_kline(coin, '1min', size=2000)
            df = pd.DataFrame(t['data'])
            new_df = df.loc[df['id'] >= lastStamp]
            new_df = new_df.loc[new_df['id'] <= run_Stamp]

            lastday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
            path = 'D:\\Robin\\UniDAX_NonObjectMM\\HistoryData\\%s\\%s.xlsx' %(lastday, coin)
            new_df.to_excel(path)

        # 重置坐标
        run_Stamp += 86400



    time.sleep(60)