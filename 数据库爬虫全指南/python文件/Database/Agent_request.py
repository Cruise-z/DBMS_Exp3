import fake_useragent
import random

# 首先实例化fake_useragent对象
ua = fake_useragent.UserAgent()
# 打印请求头
while True:
    str = ua.__getattr__(random.choice(ua.browsers))
    # print(str)
    print(str.strip())
    # print()