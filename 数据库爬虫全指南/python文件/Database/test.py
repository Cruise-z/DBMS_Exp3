# 导入需要的库
import requests
from lxml import etree
import pymysql


# 文章详情信息类
class articleData():
    def __init__(self, title, abstract, path, date):
        self.title = title  # 文章名称
        self.abstract = abstract  # 文章摘要
        self.path = path  # 文章路径
        self.date = date  # 发布时间

    def to_string(self):
        print("文章名称:" + self.title
              + ";文章摘要:" + self.abstract
              + ";文章路径:" + self.path
              + ";发布时间:" + self.date)


# 保存狗狗详情数据
# 保存数据
def saveData(DataObject):
    count = pymysql.connect(
        host='xx.xx.xx.xx',  # 数据库地址
        port=3306,  # 数据库端口
        user='xxxxx',  # 数据库账号
        password='xxxxxx',  # 数据库密码
        db='xxxxxxx'  # 数据库名
    )
    # 创建数据库对象
    db = count.cursor()
    # 写入sql
    # print("写入数据:"+DataObject.to_string())
    sql = f"insert into article_detail(title,abstract,alias,path,date) " \
          f"values ('{DataObject.title}','{DataObject.abstract}','{DataObject.path}','{DataObject.date}')"
    # 执行sql
    print(sql)
    db.execute(sql)
    # 保存修改内容
    count.commit()
    db.close()


# 爬取数据的方向
def getWebData():
    # 网站页面路径
    url = "https://blog.csdn.net/BadBoyxiaolin?spm=1000.2115.3001.5343"
    # 请求头，模拟浏览器请求
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
    }
    # 获取页面所有节点代码
    html = requests.get(url=url, headers=header)
    # 打印页面代码查看
    # print(html.text)
    # 如果乱码可以设置编码格式
    # html.encoding = 'gb2312'
    # 通过xpath获取数据对应节点
    etreeHtml = etree.HTML(html.text)
    dataHtml = etreeHtml.xpath('//*[@class="mainContent"]/div/div/div')
    # 循环获取数据
    for _ in dataHtml:
        # ''.join()是将内容转换为字符串可以后面接replace数据进行处理
        title = ''.join(_.xpath('./article/a/div[1]/h4/text()'))  # 文章标题
        # //*[@id="userSkin"]/div[2]/div/div[2]/div[1]/div[2]/div/div/div[1]/article/a/div[1]/h4
        abstract = ''.join(_.xpath('./article/a/div[2]/text()'))  # 文章摘要
        path = ''.join(_.xpath('./article/a/@href'))  # 文章路径
        date = ''.join(_.xpath('./article/a/div[3]/div/div[2]/text()')).replace(' ', '').replace('·', '').replace(
            '发布博客', '')  # 发布时间
        # 初始化文章类数据
        article_data = articleData(title, abstract, path, date)
        article_data.to_string()  # 打印数据看看是否对
        # 保存数据到数据库
        # saveData(article_data)


if __name__ == "__main__":
    getWebData()

# 〔