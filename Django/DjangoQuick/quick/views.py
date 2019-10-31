import json
import os
import sys
import threading
import time

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .bookspider import downBook, genSearchBookUrl, getCatalogues, searchBook
from .models import EBook, User


def index(request):
    if request.method == 'POST':
        # 获取到请求参数， username的写法，如果username不存在不会抛异常
        # password 会抛异常
        username = request.POST.get('username')
        password = request.POST['password']

        User(username=username, password=password).save()
        return HttpResponseRedirect('/index')

    # 业务 需求：查询出所有数据
    users = User.objects.all()
    return render(request, template_name='index.html', context={'users': users})


# 小说查询页面
def ebook(request):
    book_list = {}
    book_name = ''
    if request.method == 'GET':
        book_name = request.GET.get('bookname')
        if not book_name is None:
            print('输入的书籍名称为：%s' % book_name)
            book_list = searchBook(book_name)
        else:
            book_name = ''
        # book_list = {
        #     1: {
        #         'name': '诛仙之绝代剑仙',
        #         'author': '浮世暮秋',
        #         'url': 'http://www.biqukan.com/book/goto/id/34459',
        #         'urlid': 2722
        #     }
        # }

    return render(request, template_name='ebook.html', context={'books': book_list, 'bookname': book_name})


# 获取书籍所有章节
@csrf_exempt
def down(request, book_id):

    email = request.POST.get('e')

    # threading.Thread(target=async_down, args=(book_id, )).start()

    print('电子邮箱为->%s' % email)

    # data = {'code': 200, 'msg': '请稍后在邮箱中查收文件<br/>感谢使用！', 'result': [], 'timestamp': round(time.time() * 1000)}
    data = {'code': 200, 'msg': '因无法支付邮件服务器费用，此功能暂时不可用', 'result': [], 'timestamp': round(time.time() * 1000)}

    return JsonResponse(data)


# 开启线程异步下载
def async_down(book_id):

    catalog_url = genSearchBookUrl(book_id)

    _book_name, a_list = getCatalogues(catalog_url)

    for key, value in a_list.items():
        chapter_title = downBook(_book_name, value['catalog_url'])
        print('已下载 %s' % chapter_title)

    print('全书下载完成！')
