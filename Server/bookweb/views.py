from django.shortcuts import render
from django.http import JsonResponse
from bookweb.models import *
from django.views.decorators.csrf import csrf_exempt
import json
import encodings
# Create your views here.


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = request.body
        data = str(data , encoding = "utf-8")
        data = json.loads(data)
        name = data['name']
        password = data['password']
        print(data)
        try:
            user = Users.objects.get(Name=name)
        except Users.DoesNotExist:
            return JsonResponse({'status_code': 404, 'msg': "用户未注册"})
        else:
            if user.Password == password:
                request.session['userId'] = user.Id
                return JsonResponse({'status_code': 200, 'msg': "登录成功"})
            else:
                return JsonResponse({'status_code': 401, 'msg':"密码错误"})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = request.body
        data = str(data , encoding= "utf-8")
        data = json.loads(data)
        isuser = data['Isuser']
        if isuser:
            authtype = 0
        else:
            authtype = 1
        ismale = data['Ismale']
        if ismale:
            sex = 1
        else:
            sex = 0
        name = data['name']
        password = data['password']
        telephone = data['telephone']
        email = data['email']
        city = data['city']
        maxlength = 20
        try:
            Users.objects.get(Name=name)
        except Users.DoesNotExist:
            if len(name) < maxlength and len(password) < maxlength:
                count = Users.objects.all().count()
                count = str(count+1)
                new_user = Users(Id=count, Password=password, Name=name, Sex=sex, Telephone=telephone, City=city, Email=email, Authtype=authtype)
                new_user.save()
                return JsonResponse({'status_code': 200, 'msg': "注册成功"})
            else:
                return JsonResponse({'status_code': 402, 'msg': "用户名或密码非法"})
        else:
            return JsonResponse({'status_code': 401, 'msg': "用户已存在"})


@csrf_exempt
def logout(request):
    request.session.flush()
    return JsonResponse({'status_code': 200, 'msg': "注销成功"})

@csrf_exempt
def userBook(request):
    if request.method == 'POST':
        data = request.body
        data = str(data, encoding = "utf-8")
        data = json.loads(data)
        press = data['press']
        author = data['author']
        score_range = data['score_range']
        score_begin = score_range['score_begin']
        if score_begin == -1:
            score_begin = 0
        score_end = score_range['score_end']
        if score_end == -1:
            score_end = 10
        price_range = data['price_range']
        price_begin = price_range['price_begin']
        if price_begin == -1:
            price_begin = 0
        price_end = price_range['price_end']
        if price_end == -1:
            price_end = 2**16 #不能更大了吧
        search_data = {}
        search_data['Score__gte']=score_begin
        search_data['Score__lte'] = score_end
        search_data['Price__gte'] = price_begin
        search_data['Price__lte'] = price_end
        if press != '':
            search_data['Press'] = press
        if author != '':
            search_data['Author'] = author
        books = Summary.objects.all().filter().distinct()
        books_dict = []
        temp = {
            'ISBN' : '',
            'title' : '',
            'author': '',
            'press': '',
            'price': '',
            'score': ''
        }
        for ii in range(len(books)):
            temp['ISBN'] = books[ii].ISBN
            temp['title'] = books[ii].Title
            temp['author'] = books[ii].Author
            temp['press'] = books[ii].Press
            temp['price'] = str(books[ii].Price)
            temp['score'] = str(books[ii].Score)
            books_dict.append(temp)
            temp = {
                'ISBN': '',
                'title': '',
                'author': '',
                'press': '',
                'price': '',
                'score': ''
            }
        return JsonResponse({'books_dict':books_dict})



@csrf_exempt
def viewRemark(request):
    if request.method == 'POST':
        data = request.body
        data = str(data , encoding = "utf-8")
        data = json.loads(data)
        isbn = data['ISBN']
        book = Summary.objects.get(ISBN=isbn)
        remarks = BookComments.objects.filter(ISBN=book)
        remarks_dict = []
        temp = {
            'name': '',
            'time': '',
            'comtent': '',
            'score': ''
        }
        for i in range(len(remarks)):
            user = remarks[i].User_id
            temp['name'] = user.Name
            temp['time'] = str(remarks[i].Time)
            temp['comtent'] = str(remarks[i].Remark)
            temp['score'] = str(BookScores.objects.get(ISBN=book, User_id=user).Score)
            remarks_dict.append(temp)
            temp = {
                'name': '',
                'time': '',
                'comtent': '',
                'score': ''
            }
        return JsonResponse({'remarks_dict':remarks_dict})


@csrf_exempt
def comment(request):
    if request.method == 'POST':
        data = request.body
        data = str(data , encoding = "utf-8")
        data = json.loads(data)
        isbn = data['ISBN']
        content = data['content']
        book = Summary.objects.get(ISBN=isbn)
        user = Users.objects.get(Id=request.session['userId'])
        new_content = BookComments(ISBN=book, User_id=user, Remark=content)
        new_content.save()
        return JsonResponse({'status_code': 200, 'msg': "添加成功"})


@csrf_exempt
def mark(request):
    if request.method == 'POST':
        data = request.body
        data = str(data, encoding = "utf-8")
        data = json.loads(data)
        isbn = data['ISBN']
        score = data['score']
        book = Summary.objects.get(ISBN=isbn)
        user = Users.objects.get(Id=request.session['userId'])
        try:
            old_score = BookScores.objects.get(ISBN=book, User_id=user)
        except BookScores.DoesNotExist:
            new_score = BookScores(ISBN=book, User_id=user, Score=score)
            new_score.save()
            return JsonResponse({'status_code': 200, 'msg': "评分成功"})
        else:
            old_score.Score = score
            old_score.save()
            return JsonResponse({'status_code': 200, 'msg': "更新成功"})

@csrf_exempt
def showInfo(request):
    if request.method == 'POST':
        userid = request.session['userId']
        user = Users.objects.get(Id=userid)
        if user.Sex == 1:
            sex = '男'
        else:
            sex = '女'
        if request.method == 'POST':
            info = {
                'ID': user.Id,
                'name': user.Name,
                'telephone':user.Telephone,
                'email':user.Email,
                'city':user.City,
                'authType':user.Authtype,
                'sex':sex
            }
            return JsonResponse({'info': info})


@csrf_exempt
def updateInfo(request):
    if request.method == 'POST':
        data = request.body
        data = str(data , encoding = "utf-8")
        data = json.loads(data)
        new_name = data['new_name']
        telephone = data['telephone']
        email = data['email']
        city = data['city']
        sex = data['sex']
        userid = request.session['userId']
        user = Users.objects.get(Id=userid)
        user.Name = new_name
        user.Telephone = telephone
        user.Email = email
        user.City = city
        if sex == '男':
            user.Sex = 1
        else:
            user.Sex = 0
        user.save()
        return JsonResponse({'status_code': 200, 'msg': "修改成功"})



@csrf_exempt
def updatePassword(request):
    if request.method == 'POST':
        data = request.body
        data = str(data , encoding = "utf-8")
        data = json.loads(data)
        originPass = data['originPass']
        newPass = data['newPass']
        userid = request.session['userId']
        user = Users.objects.get(Id=userid)
        maxlength = 20
        if user.Password == originPass:
            if len(newPass) < maxlength:
                user.Password = newPass
                user.save()
                return JsonResponse({'status_code': 200, 'msg': "修改成功"})
            else:
                return JsonResponse({'status_code': 402, 'msg': "新密码非法"})
        else:
            return JsonResponse({'status_code': 401, 'msg': "原密码错误"})


@csrf_exempt
def deleteBook(request):
    if request.method == 'POST':
        data = request.body
        data = str(data , encoding = "utf-8")
        data = json.loads(data)
        isbn = data['ISBN']
        book = Summary.objects.get(ISBN=isbn)
        adminid = request.session['userId']
        admin = Users.objects.get(Id=adminid)
        if admin.Authtype == 0:
            return JsonResponse({'status_code': 1, 'msg': "下架失败"})
        else:
            book.delete()
            return JsonResponse({'status_code': 0, 'msg': "下架成功"})


@csrf_exempt
def deleteComment(request):
    if request.method == 'POST':
        data = request.body
        data = str(data , encoding = "utf-8")
        data = json.loads(data)
        isbn = data['ISBN']
        username = data['username']
        user = Users.objects.get(Name=username)
        remark = BookComments.objects.get(ISBN=isbn, User_id=user)
        adminid = request.session['userId']
        admin = Users.objects.get(Id=adminid)
        if admin.Authtype == 0:
            return JsonResponse({'status_code': 1, 'msg': "删评失败"})
        else:
            remark.delete()
            return JsonResponse({'status_code': 0, 'msg': "删评成功"})


@csrf_exempt
def addBook(request):
    print("访问")
    if request.method == 'POST':
        print("进入")
        data = request.body
        data = str(data , encoding = "utf-8")
        data = json.loads(data)
        isbn = data['ISBN']
        title = data['title']
        author = data['author']
        press = data['press']
        price = float(data['price'])
        print(data)
        adminid = request.session['userId']
        admin = Users.objects.get(Id=adminid)
        if admin.Authtype == 0:
            return JsonResponse({'status_code': 1, 'msg': "上架失败"})
        else:
            # new_book = Summary(ISBN=isbn, Title=title, Author=author, Price=price, Press=press)
            new_book = Summary(ISBN=isbn, Title=title, Author=author, Price=price, Press=press, Num_of_scorers=0, Num_of_comments=0)
            new_book.save()
            return JsonResponse({'status_code': 0, 'msg': "上架成功"})
