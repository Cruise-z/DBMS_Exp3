# publish/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # path('url_name', api_name)
    # 这是一个样例，指定路由名为url_name，对应处理函数为当前app内views.py中的api_name
    path('login', login),
    path('register', register),
    path('logout', logout),
    path('userBook', userBook),
    path('viewRemark', viewRemark),
    path('comment', comment),
    path('mark', mark),
    path('showInfo', showInfo),
    path('updateInfo', updateInfo),
    path('updatePassword', updatePassword),
    path('deleteBook', deleteBook),
    path('deleteComment', deleteComment),
    path('addBook', addBook)
]
