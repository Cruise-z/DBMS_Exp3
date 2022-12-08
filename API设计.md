## API设计

### 1、登录功能

url设计：bookweb/login

功能：实现两种登录模式：管理员、用户

			实现结果：成功登录，密码错误，用户不存在

前端信息：两个字符串，前端保证数据不为空

```
"name"：用户名，String

"password"：密码，String
```

后端返回：json文件

```json
"status_code"：int, 200登录成功，404表示用户未注册，401表示密码错误
```



### 2、注册功能

url设计：bookweb/register

功能：实现两种注册模式：用户、管理员

			实现结果：成功注册，用户已存在，密码非法

前端信息：两个字符串，前端保证数据不为空

```json
"Isuser"：表示注册类型，BOOL,ture是普通用户,false是管理员

"Ismale": 性别，BOOL,ture是男，false是女

"name"：用户名，String

"password"：密码，String

"telephone": 电话，string

"email": 邮箱，string

"city": 城市，string
```

后端返回：json文件

```json
"status_code"：int, 200注册成功，401表示用户已存在，402表示密码非法
```

说明：注册成功不用后端自动登录，注册成功后要用户再登录才可以登录成功。

### 3、注销功能

url设计：bookweb/logout

功能：实现用户的退出登录

```
		实现结果：成功注销
```

前端信息：无

```json
{}
```

后端返回：json文件

```json
"status_code": int, 200注销成功
```

### 用户API

### 1、用户查看书籍信息

url设计：bookweb/userBook

功能：给用户展示**已经上架**的书籍详细信息

前端信息：

```json
{
    "press"			: 表示出版社	,String (前端为下拉列表形式),
    "author"		: 表示作者	, String
    "score_range"	: {
    					"score_begin"	：表示开始区间	, Float/Double(一位小数) -1代表无下限
    					"score_end"		: 表示结束区间 , Float/Double(一位小数) -1代表无上限
						}
	"price_range"	: {
        				"price_begin"	：表示开始区间	, Float/Double(一位小数) -1代表无下限
    					"price_end"		: 表示结束区间 , Float/Double(一位小数) -1代表无上限
    					}
}
```



后端返回：

```json
"ISBN": 书籍ISBN

"title": 标题，String

"author": 作者，String

"press": 出版社，String

"price": 价格（保留两位小数），String，允许为空值

"score": 平均分数（保留一位小数），String，允许为空值
```

**返回值为一个list**，其中每个list的元素都是上述的字典形式

说明：对于后端，是可以判断某个前端信息是否缺失的：

![image-20221205194740951](C:\Users\vip\AppData\Roaming\Typora\typora-user-images\image-20221205194740951.png)


### 2、查看书籍评论

url设计：bookweb/viewRemark/

功能：查看一本书籍的所有评论

前端信息：

```json
"ISBN"：书籍ISBN
```

后端返回：

```json
"name": 用户名，string

"time": 评论时间，string

"content": 评论内容，string

"score":该用户对本书的评分（保留一位小数），Double/Float，允许为空值
```

**一个list**，每个list的表项都是上述的字典



### 3、评论书籍

url设计：bookweb/comment/

功能：用户对一本书发布评论

前端信息：

```json
"ISBN" : ISBN

"time": 评论时间，string

"content": 评论内容，string

```

后端返回：

``` json
"status_code": int, 200添加成功
```

说明：后端通过存的用户信息，向数据库添加时自动附上用户名



### 4、给书籍打分

url设计：bookweb/mark/

功能：用户对一本书打分

前端信息：

```json
"ISBN" : ISBN

"score":该用户对本书的评分，int，只能为0-10的整数。
```

后端返回：

```json
"status_code": int, 200添加成功
```

说明：同一用户重复打分，则以最后一次为准，即覆盖。

### 5、查看个人信息

url设计：bookweb/showInfo

功能：查看个人信息

前端信息：无

后端返回：

```json
"ID": 用户ID，string

"name":用户名，string

"telephone": 电话，string

"email": 邮箱，string

"city": 城市，string

"authType": 用户类型，Int,1表示管理员，0表示普通用户

"sex": 性别，string——男,女
```



### 6、更新个人信息

url设计：bookweb/updateInfo

功能：更新个人信息（一次性提交全部属性）

前端信息：

```json
"new_name": 新用户名

"telephone": 新电话，string

"email": 新邮箱，string

"city": 新城市，string

"sex": 性别，string——男,女
```

后端返回：

``` json
"status_code":int,200 修改成功 ，404 更新失败
```

说明：后端更新信息时可能因为一些限制导致更新失败，此时返回404, 前端检测用户名不为空（后端也可以检测，防止前端绕过，更安全）



### 7、更新个人密码

url设计：bookweb/updatePassword

功能：改密码

前端信息：

```json
"originPass":原密码

"newPass":新密码
```

后端返回：

```json
"status_code"：int, 200修改成功，401表示原密码错误，402表示新密码不合法
```



### 管理员API



### 1、管理员下架书籍

url设计：bookweb/deleteBook

功能：下架书籍

前端信息：

```json
"ISBN": string
```

后端信息：

```json
"status_code"：int, 0成功，1失败
```

### 2、管理员删评

url设计：bookweb/deleteComment

功能：删除特定评论

前端信息：

```json
"ISBN": string
"username": 用户名, string
"timeStamp": 时间戳, string
```

后端信息：

```json
"status_code"：int, 0成功，1失败
```
<<<<<<< HEAD
=======

>>>>>>> e6c11dcc84cf943936275f0352729755b6558cfa
