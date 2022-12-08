from IPS.ip_api import run as api_run
from IPS.ip_collection import run as col_run
from IPS.ip_verify import run as ver_run
from multiprocessing import Process
import os

def run():
    # 启动三个进程
    p1 = Process(target=api_run)
    p2 = Process(target=col_run)
    p3 = Process(target=ver_run)

    p1.start()
    p2.start()
    p3.start()
    return p1.pid, p2.pid, p3.pid

def exit(p1, p2, p3):
    os.kill(p1, 9)
    os.kill(p2, 9)
    os.kill(p3, 9)



if __name__ == '__main__':
    run()

# https://blog.csdn.net/weixin_56382303/article/details/124563124 搭建免费代理IP池
# https://www.cnblogs.com/ruozhisi/p/12199311.html redis修改requirepass 参数 改密码