import datetime
import time
import sys
import subprocess


# # 参与报价币种
# _code = sys.argv[1]
# _envo = sys.argv[2]
# _data = sys.argv[3]

path = 'D:\\Robin\\UniDAX_NonObjectMM\\Kline\\RunDayKline.py'


class run_action():
    def __init__(self, cmd):
        self.cmd = cmd
        self.p = None
        self.begin_time = datetime.datetime.now()
        self.count = 0

        # 运行
        self.run()

        try:
            while True:
                time.sleep(60)
                self.poll = self.p.poll() #判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出

                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if self.poll is None:
                    print(now_time + '  ' + ": NORMAL")
                else:
                    print(now_time + '  ' + ": STOP,TRY RE-OPEN")
                    self.run()
        except Exception as e:
            print('---->except<mm_action>', e)

    def run(self):
        print('start OK!')
        self.p = subprocess.Popen(['python', '%s' % self.cmd],
                                  stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)
        # self.p = subprocess.Popen(['python', '%s' % [self.cmd, self.code, self.envo,% self.data],
        #                           stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)


app = run_action(path)