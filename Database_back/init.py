import pymysql


def init_DB():
    # 连接root数据库
    root = pymysql.connect(
        host='localhost',  # 数据库地址
        port=3306,  # 数据库端口
        user='root',  # 数据库账号
        password='mysql1005',  # 数据库密码
        charset='utf8'
    )
    r = root.cursor()
    # 创建数据库并建立用户，授予权限
    sql_create_db = f"create database IF NOT EXISTS book_manage_system;"
    sql_create_user = f"create user 'bms_admin'@'localhost' identified by '123456';"
    sql_grant_permission = f"grant all on book_manage_system.* to 'bms_admin'@'localhost';"
    sql_set_env = f"set global log_bin_trust_function_creators = 1;"
    r.execute(sql_create_db)
    r.execute(sql_create_user)
    r.execute(sql_grant_permission)
    r.execute(sql_set_env)

    root.commit()
    r.close()

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
    # 写入sql
    # print("写入数据:"+DataObject.to_string())

    # 创建总表
    sql_summary_schema = f"CREATE TABLE IF NOT EXISTS summary (" \
                         f"ISBN char(13) not null," \
                         f"Title varchar(255)," \
                         f"Author varchar(255)," \
                         f"Price double(7, 2)," \
                         f"Press varchar(255)," \
                         f"Score double(3,1)," \
                         f"Num_of_scorers INT UNSIGNED," \
                         f"Num_of_comments INT UNSIGNED," \
                         f"PRIMARY KEY (ISBN)" \
                         f")DEFAULT CHARSET=utf8;"
    db.execute(sql_summary_schema)

    # 创建用户表
    sql_user_schema = f"CREATE TABLE IF NOT EXISTS users (" \
                      f"ID varchar(255) not null," \
                      f"Password varchar(255)," \
                      f"Name varchar(255)," \
                      f"Sex TINYINT(1)," \
                      f"Telephone varchar(255)," \
                      f"City varchar(255)," \
                      f"Email varchar(255)," \
                      f"Authtype TINYINT(1)," \
                      f"PRIMARY KEY (ID)" \
                      f")DEFAULT CHARSET=utf8;"
    # sex 1表示男性; Authtype 1表示为管理员
    db.execute(sql_user_schema)

    # 创建书籍-评论表
    sql_book_com_schema = f"CREATE TABLE IF NOT EXISTS book_comments (" \
                          f"ISBN char(13) not null," \
                          f"User_id varchar(255)," \
                          f"Time DATETIME," \
                          f"Remark varchar(255)," \
                          f"PRIMARY KEY (ISBN, User_id, Time)," \
                          f"CONSTRAINT ISBNfk_book_com " \
                          f"FOREIGN KEY(ISBN) REFERENCES summary(ISBN)," \
                          f"CONSTRAINT IDfk_book_com " \
                          f"FOREIGN KEY(User_id) REFERENCES users(ID)" \
                          f")DEFAULT CHARSET=utf8;"
    db.execute(sql_book_com_schema)

    # 创建书籍-评分表
    sql_book_sco_schema = f"CREATE TABLE IF NOT EXISTS book_scores (" \
                          f"ISBN char(13) not null," \
                          f"User_id varchar(255)," \
                          f"Score double(3,1)," \
                          f"PRIMARY KEY (ISBN, User_id)," \
                          f"CONSTRAINT ISBNfk_book_sco " \
                          f"FOREIGN KEY(ISBN) REFERENCES summary(ISBN)," \
                          f"CONSTRAINT IDfk_book_sco " \
                          f"FOREIGN KEY(User_id) REFERENCES users(ID)" \
                          f")DEFAULT CHARSET=utf8;"
    db.execute(sql_book_sco_schema)

    # 创建总表中评分、评论人数触发器
    # 这里每个用户对一本书只有一次评论机会，评论之后不可再进行评论
    score_trigger = f"CREATE TRIGGER score_trigger " \
                    f"AFTER INSERT ON book_scores " \
                    f"FOR EACH ROW " \
                    f"BEGIN " \
                    f"UPDATE summary " \
                    f"SET Score = (Score*Num_of_scorers+new.score)/(Num_of_scorers+1)," \
                    f"Num_of_scorers = Num_of_scorers+1 " \
                    f"WHERE ISBN = new.ISBN;" \
                    f"END;"
    db.execute(score_trigger)

    # 创建总表中评论的触发器
    comment_trigger = f"CREATE TRIGGER comment_trigger " \
                      f"AFTER INSERT ON book_comments " \
                      f"FOR EACH ROW " \
                      f"BEGIN " \
                      f"UPDATE summary " \
                      f"SET Num_of_comments = Num_of_comments+1 " \
                      f"WHERE ISBN = new.ISBN;" \
                      f"END;"
    db.execute(comment_trigger)

    admin.commit()
    db.close()


if __name__ == "__main__":
    init_DB()
