# 配置文件

# proxy_redis
# redis主机ip地址
REDIS_HOST = "127.0.0.1"
# redis端口号
REDIS_PORT = 6379
# redis数据库编号
REDIS_DB = 1
# redis的密码
REDIS_PASSWORD = "123456"

# redis的key
REDIS_KEY = "proxy_ip"

# 默认的ip分值
DEFAULT_SCORE = 50
# 满分
MAX_SCORE = 100

# ip_verify
# 一次检测ip的数量
SEM_COUNT = 30

# https://blog.csdn.net/weixin_38858749/article/details/124686796 redis设置用户名和密码
# https://blog.csdn.net/oooo2316/article/details/107545700 Windows编译安装Redis 6.0