# 导入需要的库
import re
import random
import time
import requests
from lxml import etree
import pymysql
import fake_useragent
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from IPS import get_IPS


class BookData:
    def __init__(self, ISBN, title, author, price, press, score, Num_of_scorers):
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.price = price
        self.press = press
        self.score = score
        self.Num_of_scorers = Num_of_scorers

    def to_string(self):
        print("ID(ISBN):" + self.ISBN
              + " 书名:" + self.title
              + " 作者:" + self.author
              + " 价格:" + self.price
              + " 出版社:" + self.press
              + " 评分:" + self.score
              + " 评分人数:" + self.Num_of_scorers)


def init_DB():
    count = pymysql.connect(
        host='localhost',  # 数据库地址
        port=3306,  # 数据库端口
        user='admin',  # 数据库账号
        password='123456',  # 数据库密码
        db='book_db'  # 数据库名
    )
    # 创建数据库对象
    db = count.cursor()
    # 写入sql
    # print("写入数据:"+DataObject.to_string())
    '''
    # 创建数据库并建立用户，授予权限
    sql_login_root = f"mysql -u root -p'123456'"
    sql_create_db = f"create database book_db;"
    sql_create_user = f"create user 'admin'@'localhost' identified by '123456'"
    sql_grant_permission = f"grant all on book_db.* to 'admin'@'localhost'"
    '''
    sql_schema = f"CREATE TABLE IF NOT EXISTS summary (" \
                 f"ISBN char(13) not null," \
                 f"title varchar(255)," \
                 f"author varchar(255)," \
                 f"price double(7, 2)," \
                 f"press varchar(255)," \
                 f"score double(3,1)," \
                 f"Num_of_scorers INT UNSIGNED," \
                 f"PRIMARY KEY (ISBN)" \
                 f")DEFAULT CHARSET=utf8;"
    db.execute(sql_schema)
    count.commit()
    db.close()


# 保存数据
def saveData(DataObject):
    count = pymysql.connect(
        host='localhost',  # 数据库地址
        port=3306,  # 数据库端口
        user='admin',  # 数据库账号
        password='123456',  # 数据库密码
        db='book_db'  # 数据库名
    )
    # 创建数据库对象
    db = count.cursor()
    # 写入sql
    # print("写入数据:"+DataObject.to_string())
    sql_data = f"replace into summary(ISBN, title, author, price, press, score, Num_of_scorers) " \
               f"values ('{DataObject.ISBN}','{DataObject.title}','{DataObject.author}'," \
               f"'{DataObject.price}','{DataObject.press}','{DataObject.score}'," \
               f"'{DataObject.Num_of_scorers}')"
    # 执行sql
    db.execute(sql_data)
    # 保存修改内容
    count.commit()
    db.close()


def get_proxys():
    ua = fake_useragent.UserAgent()

    resp = requests.get(
        url="http://127.0.0.1:5800/get_proxy",
        headers={"user-agent": (ua.__getattr__(random.choice(ua.browsers))).strip(), 'Connection': 'close'},
        verify=False
    )
    ips = resp.json()
    return ips["ip"][0]


def test_ip():
    url = "https://book.douban.com/"
    ua = fake_useragent.UserAgent()
    proxys = get_proxys()
    available_proxys = []
    for proxy_ip in proxys:
        try:
            proxy = {
                "http:": "http://" + proxy_ip,
                "https:": "https://" + proxy_ip
            }
            resp = requests.get(
                url,
                proxies=proxy,
                headers={"user-agent": (ua.__getattr__(random.choice(ua.browsers))).strip(), 'Connection': 'close'},
                verify=False
            )
            # resp.encoding = "utf-8"
            '''这里用来验证ip能否成功得到的豆瓣网页代码'''
            # https://blog.csdn.net/hpwzjz/article/details/108385568 文本高亮输出
            judge = etree.HTML(resp.text)
            if judge is not None:
                inf = re.findall(r'.*?(err).*?', resp.text)
                inf += re.findall(r'.*?(异常).*?', resp.text)
                inf += re.findall(r'.*?(登录跳转).*?', resp.text)
                print(inf)
                if len(inf) == 0:
                    print(resp.text)
                    print('\033[1;31;43m%s\033[0m' % "test successful!!!!!!")
                    print('\033[1;31;43m%s\033[0m' % proxy_ip)
                    available_proxys.append(proxy)
                else:
                    print("ip:" + '\033[1;31;43m%s\033[0m' % proxy_ip + "被封")
            else:
                print('\033[1;31;43m%s\033[0m' % "代理无法得到网页源码，无法使用！")
        except:
            print('\033[1;31;43m%s\033[0m' % "验证ip程序抛出错误")
    return available_proxys


# 爬取数据的方向
def getWebData():
    # 网站页面路径
    # 整合多个网页上的数据(共15页)
    url = []
    for cnt in range(8, 11):
        url.append('https://book.douban.com/latest?subcat=%E5%85%A8%E9%83%A8&p=' + str(cnt))

    # 请求头，模拟浏览器请求
    ua = fake_useragent.UserAgent()
    '''
    agent = ua.__getattr__(random.choice(ua.browsers))
    header = {"user-agent": agent}
    print(header)
    '''

    # pid1, pid2, pid3 = get_IPS.run()
    # time.sleep(270)
    # available_proxy = test_ip()
    # get_IPS.exit(pid1, pid2, pid3)
    # if not available_proxy:
    #     exit(-1)

    init_DB()
    for page in url:
        # 获取页面所有节点代码
        html = requests.get(
            url=page,
            # proxies=random.choice(available_proxy),
            headers={"user-agent": (ua.__getattr__(random.choice(ua.browsers))).strip(), 'Connection': 'close'},
            verify=False
        )
        '''
        # 打印页面代码查看
        print(html.text)
        # 如果乱码可以设置编码格式
        html.encoding = 'gb2312'
        '''
        # 通过xpath获取数据对应节点
        etreeHtml = etree.HTML(html.text)
        '''
        通过抓取网站界面上的块(数据容器)来找到循环抓取的源目录
        这个网站界面上的第1个块  //*[@id="content"]/div/div[1]/ul/li[1]
        这个网站界面上的第4个块  //*[@id="content"]/div/div[1]/ul/li[4]
        '''
        dataHtml = etreeHtml.xpath('//*[@id="content"]/div/div[1]/ul/li')
        # 循环获取数据
        for _ in dataHtml:
            '''
            我们寻找这些块所对应的书籍详细内容对应的地址
            结合上面的源目录还有xpath抓取我们可以得到书籍详细内容对应的xpath基于源地址dataHtml的部分路径
            //*[@id="content"]/div/div[1]/ul/li[1]/div[2]/h2/a
            //*[@id="content"]/div/div[1]/ul/li[2]/div[2]/h2/a
            @href可以获取<a>下的链接地址，也就是我们想要的书籍详细内容对应的地址
            '''
            detail_page_url = str(_.xpath('./div[2]/h2/a/@href'))[2:-2]  # _.xpath()是list类型，将其转化为str类型
            # print(detail_page_url)
            while True:
                html_detail = requests.get(
                    url=detail_page_url,
                    # proxies=random.choice(available_proxy),
                    headers={"user-agent": (ua.__getattr__(random.choice(ua.browsers))).strip(), 'Connection': 'close'},
                    verify=False
                )
                etreeHtml_detail = etree.HTML(html_detail.text)
                # print(html_detail.text)
                detail_path = str(etreeHtml_detail.xpath('//*[@id="info"]/text()'))
                if detail_path != '[]':
                    break
            '''现在收集书籍的各属性信息'''
            ISBN_path = str(re.findall(r'.*?(978\d{10}).*?', detail_path)[0])
            # print(ISBN_path)
            author_path = str(
                etreeHtml_detail.xpath('//*[@id="info"]/span[1]/a[1]/text()')
            )[2:-2].replace(' ', '')
            author_path = re.sub(r'[【(（〔［]', '[', author_path)
            author_path = re.sub(r'[】)）〕］]', ']', author_path)
            # print(author_path)
            press_path = str(
                etreeHtml_detail.xpath('//*[@id="info"]/a[1]/text()')
            )[2:-2].strip()
            # print(press_path)
            score_path = str(
                etreeHtml_detail.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')
            )[3:-3].strip()
            # print(score_path)
            Num_of_sco_path = str(
                etreeHtml_detail.xpath(
                    '//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span/text()')
            )[2:-2].strip()
            # print(Num_of_sco_path)
            '''我们可以在dataHtml这个初始的第一个界面上找到书名和价格信息'''
            title_path = str(
                _.xpath('./div[2]/h2/a/text()')
            )[2:-2]
            # print(title_path)
            price_path = str(
                _.xpath('./div[2]/div[1]/span[1]/a/text()')
            )
            price_path = re.findall(r"纸质版 (.+?)元", price_path)
            '''如果dataHtml页面上找不到价格信息，就进入detail_page_url链接对应的细节网页上查看价格'''
            if len(price_path) == 0:
                price_path = re.findall(r'.*?(\d+\.\d{2})', detail_path)
                price_path += re.findall(r'.*?(\d+)元', detail_path)
                if len(price_path) == 0:
                    detail2_path = str(etreeHtml_detail.xpath('//*[@id="buyinfo-printed"]/text()'))
                    price_path = re.findall(r'.*?(\d+\.\d{2})', detail2_path)
                    price_path += re.findall(r'.*?(\d+)元', detail2_path)
                price_path = str(price_path[0])
            # //*[@id="buyinfo-printed"]/ul/li[2]/div/div[2]/div[1]/a/span
            # ''.join()是将内容转换为字符串可以后面接replace数据进行处理
            ISBN = ''.join(ISBN_path)  # 书籍ID
            title = ''.join(title_path)  # 书名
            author = ''.join(author_path)  # 作者
            price = ''.join(price_path)  # 价格
            press = ''.join(press_path)  # 出版社
            score = ''.join(score_path)  # 评分
            Num_of_sco = ''.join(Num_of_sco_path)  # 评论数
            if score == '':
                score = '0.0'
            if Num_of_sco == '':
                Num_of_sco = '0'
            if price == '':
                price = '-1'
            # 初始化文章类数据
            Book_Data = BookData(ISBN, title, author, price, press, score, Num_of_sco)
            Book_Data.to_string()  # 打印数据看看是否对
            # 保存数据到数据库
            saveData(Book_Data)


if __name__ == "__main__":
    getWebData()

# https://zhuanlan.zhihu.com/p/139596371
# https://www.lfd.uci.edu/~gohlke/pythonlibspip
