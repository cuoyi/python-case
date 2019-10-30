from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import User, EBook

from .bookspider import searchBook


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
    return render(request,
                  template_name='index.html',
                  context={'users': users})


# 小说查询页面
def ebook(request):
    book_list = {}
    book_name = ''
    if request.method == 'GET':
        book_name = request.GET.get('bookname')
        if not book_name is None:
            print('输入的书籍名称为：%s' % book_name)
            book_list = searchBook(book_name)
        # book_list = {
        #     1: {
        #         'name': '诛仙之绝代剑仙',
        #         'author': '浮世暮秋',
        #         'url': 'http://www.biqukan.com/book/goto/id/34459'
        #     }
        # }

    return render(request,
                  template_name='ebook.html',
                  context={
                      'books': book_list,
                      'bookname': book_name
                  })
