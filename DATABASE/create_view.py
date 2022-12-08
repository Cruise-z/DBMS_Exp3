import pymysql

def create_view():
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

    # 创建书籍基本信息表
    create_basicInf = f"CREATE VIEW books_basic_inf " \
                   f"AS SELECT ISBN, Title, Author, Press FROM summary;"
    db.execute(create_basicInf)

    # 创建书籍-出版社表
    create_book_press = f"CREATE VIEW book_press_inf " \
                   f"AS SELECT ISBN, Title, Press FROM summary;"
    db.execute(create_book_press)

    # 创建书籍-出版社表
    create_book_price = f"CREATE VIEW book_price_inf " \
                        f"AS SELECT ISBN, Title, Price FROM summary;"
    db.execute(create_book_price)

    # 创建书籍-评分表
    create_book_score = f"CREATE VIEW book_score_inf " \
                        f"AS SELECT ISBN, Title, Score FROM summary;"
    db.execute(create_book_score)

    # 创建书籍-评分表
    create_book_author = f"CREATE VIEW book_author_inf " \
                        f"AS SELECT ISBN, Title, Author FROM summary;"
    db.execute(create_book_author)

    admin.commit()
    db.close()


if __name__ == "__main__":
    create_view()