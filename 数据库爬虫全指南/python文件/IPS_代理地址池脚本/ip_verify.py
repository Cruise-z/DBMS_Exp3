# 代理IP的验证
from IPS.proxy_redis import ProxyRedis
from IPS.settings import *
import asyncio
import aiohttp
import time


async def verify_one(ip, sem, red):
    print(f"开始检测{ip}")
    timeout = aiohttp.ClientTimeout(total=10)  # 设置超时时间，超过10秒就报错
    try:
        async with sem:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://www.baidu.com/", proxy="http://" + ip, timeout=timeout) as resp:  # 简单发送一个请求
                    page_source = await resp.text()
                    if resp.status in [200, 302]:  # 验证状态码
                        # 将分值拉满
                        red.set_max_score(ip)
                        print(f"检测到{ip}是可用的")
                    else:
                        red.reduce_score(ip)
                        print(f"检测到{ip}是不可用的， 扣10分")
    except Exception as E:
        print("ip检验时出错了", E)
        red.reduce_score(ip)
        print(f"检测到{ip}是不可用的， 扣10分")


async def main(red):
    # 查询全部ip
    all_proxy = red.get_all_proxy()
    sem = asyncio.Semaphore(SEM_COUNT)  # 控制并发量
    tasks = []
    for ip in all_proxy:
        tasks.append(asyncio.create_task(verify_one(ip, sem, red)))
    if tasks:
        await asyncio.wait(tasks)


def run():
    red = ProxyRedis()
    time.sleep(10)
    while True:
        try:
            asyncio.run(main(red))
            time.sleep(100)
        except Exception as e:
            print("校验时报错了", e)
            time.sleep(100)


if __name__ == '__main__':
    run()
