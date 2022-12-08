import pymysql


def execute_fromfile(filename, cursor):  # 封装一个读取sql文件中的sql语句，并执行语句的方法
    fd = open(filename, 'r', encoding='utf-8')  # 以只读的方式打开sql文件
    sqlfile = fd.read()  # 读取文件内容
    fd.close()
    sqlcommamds = sqlfile.split(';')  # 以;切割文件内容，获取单个sql语句
    sqlcommamds.pop()
    for command in sqlcommamds:
        try:
            cursor.execute(command)
            # cur = cursor.execute(command)  # 执行每个sql语句
            # print('sql执行成功:', cur)
        except Exception as msg:
            print("错误信息： ", msg)

    print('sql执行完成')


def insert_data():
    admin = pymysql.connect(
        host='localhost',  # 数据库地址
        port=3306,  # 数据库端口
        user='bms_admin',  # 数据库账号
        password='123456',  # 数据库密码
        db='book_manage_system',  # 数据库名
        charset='utf8'
    )
    # 创建数据库对象
    db = admin.cursor()
    execute_fromfile('./summary.sql', db)
    admin.commit()
    db.close()

if __name__ == "__main__":
    insert_data()