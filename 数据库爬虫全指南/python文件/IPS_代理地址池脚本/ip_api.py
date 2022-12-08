# 代理的IP的api接口
from IPS.proxy_redis import ProxyRedis
from sanic import Sanic, json
from sanic_cors import CORS

# 1. 创建app
app = Sanic("ip")
# 2. 解决跨域
CORS(app)

red = ProxyRedis()

# 3. 准备处理http请求的函数
@app.route("/get_proxy")  # 路由配置
def dispose(rep):
    ip_list = red.get_avail_proxy()
    return json({"ip": ip_list})  # 返回给客户端


def run():
    app.run(host="127.0.0.1", port=5800)


if __name__ == '__main__':
    run()
