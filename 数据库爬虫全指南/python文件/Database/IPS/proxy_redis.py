# redis的各种操作

from redis import Redis
from IPS.settings import *



class ProxyRedis:

    # 连接redis
    def __init__(self):
        self.red = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            username="default",
            password=REDIS_PASSWORD,
            decode_responses=True
        )

    # 存储ip
    def add_proxy_ip(self, ip):
        # 判断是否有ip
        if not self.red.zscore(REDIS_KEY, ip):
            self.red.zadd(REDIS_KEY, {ip: DEFAULT_SCORE})
            print("采集到了IP地址了", ip)
        else:
            print("采集到了IP地址了", ip, "但是已经存在")

    # 查询所有ip
    def get_all_proxy(self):
        return self.red.zrange(REDIS_KEY, 0, -1)

    # 将分值拉满
    def set_max_score(self, ip):
        self.red.zadd(REDIS_KEY, {ip: MAX_SCORE})

    # 降低分值
    def reduce_score(self, ip):
        # 查询分值
        score = self.red.zscore(REDIS_KEY, ip)
        # 如果有分值，扣分
        if score > 0:
            self.red.zincrby(REDIS_KEY, -10, ip)
        else:  # 分值没有则删除
            self.red.zrem(REDIS_KEY, ip)

    # 查询可用ip
    def get_avail_proxy(self):
        lis = []
        ips = self.red.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE, 0, -1)
        if ips:
            lis.append(ips)
            return lis
        else:
            ips = self.red.zrangebyscore(REDIS_KEY, DEFAULT_SCORE + 1, MAX_SCORE - 1, 0, -1)
            if ips:
                lis.append(ips)
                return lis
            else:
                print("没有可用ip")
                return None
