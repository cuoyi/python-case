from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import User

# Create your views here.
# def index(request):
#     return HttpResponse('success')


def index(request):
    # return render(request, 'index.html')

    # 判断是否是post请求
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
