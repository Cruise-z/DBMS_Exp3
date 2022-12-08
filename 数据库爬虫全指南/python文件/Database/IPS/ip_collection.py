# 代理IP的采集
from IPS.proxy_redis import ProxyRedis
import requests
from lxml import etree
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

# 采集快代理
def get_kuai_ip(red):
        url = "https://www.kuaidaili.com/free/intr/1/"
        resp = requests.get(url, headers=headers)
        tree = etree.HTML(resp.text)
        trs = tree.xpath("//table/tbody/tr")
        for tr in trs:
            ip = tr.xpath("./td[1]/text()")  # ip地址
            port = tr.xpath("./td[2]/text()")  # 端口
            if not ip:
                continue
            ip = ip[0]
            port = port[0]
            proxy_ip = ip + ":" + port
            red.add_proxy_ip(proxy_ip)  # 增加ip地址


# 采集66免费代理网
def get_66_ip(red):
    url = "http://www.66ip.cn/areaindex_1/1.html"
    resp = requests.get(url, headers=headers)
    tree = etree.HTML(resp.text)
    trs = tree.xpath("//table//tr")[1:]
    for tr in trs:
        ip = tr.xpath("./td[1]/text()")  # ip地址
        port = tr.xpath("./td[2]/text()")  # 端口
        if not ip:
            continue
        ip = ip[0]
        port = port[0]
        proxy_ip = ip + ":" + port
        red.add_proxy_ip(proxy_ip)  # 增加ip地址

# 采集高可用全球免费代理IP库
def get_quan_ip(red):
    url = "https://ip.jiangxianli.com/?page=1"
    resp = requests.get(url, headers=headers)
    tree = etree.HTML(resp.text)
    trs = tree.xpath("//table//tr")
    for tr in trs:
        ip = tr.xpath("./td[1]/text()")  # ip地址
        port = tr.xpath("./td[2]/text()")  # 端口
        if not ip:
            continue
        ip = ip[0]
        port = port[0]
        proxy_ip = ip + ":" + port
        red.add_proxy_ip(proxy_ip)  # 增加ip地址


def run():
    red = ProxyRedis()  # 创建redis存储
    while True:
        try:
            get_kuai_ip(red)  # 采集快代理
            get_66_ip(red)  # 采集66免费代理
            get_quan_ip(red)  # 采集全球免费ip代理库
        except:
            print("出错了")
        time.sleep(60)  # 每分钟跑一次


if __name__ == '__main__':
    run()
