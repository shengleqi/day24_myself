from django.shortcuts import render,HttpResponse,redirect

from rbac.forms import  HostModelsForm,LoginForm,RegForm,UserInfoModelsForm

from rbac.service.init_permission import init_permission

# Create your views here.
from django.conf import settings
from rbac import  models
from utils.md5 import md5
from rbac import  forms
import  json

def index(request):
    username=request.session[settings.USER_SESSION_KEY]['username']
    print("username",username)
    return render(request, "index.html", {"username":username})

def reg(request):
    if request.method=="GET":
        form = RegForm()
        return render(request, 'reg.html', locals())
    else:
        form = RegForm(request.POST)
        if form.is_valid():
            form.cleaned_data['password'] = md5(form.cleaned_data['password'])
            print("form.cleaned_data==::",form.cleaned_data["username"])
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user = models.UserInfo.objects.create(username=username,password=password)
            return redirect("/login/")
        return render(request, 'reg.html', locals())

    return redirect("/reg/")

def login(request):
    if request.method=='GET':
        form=LoginForm()
        return  render(request,"login.html",{"form":form})
    else:
        form=LoginForm(request.POST)
        if form.is_valid():
            form.cleaned_data["password"]=md5(form.cleaned_data["password"])
            print("form.cleaned_data:",form.cleaned_data)
            user = models.UserInfo.objects.filter(**form.cleaned_data).first()
            if user:
                #写入session
                request.session[settings.USER_SESSION_KEY]={'id': user.pk, 'username': user.username}

                # 权限初始化
                init_permission(user, request)

                return redirect("/hosts/")
            else:
                form.add_error('password', '用户名或密码错误')
        return render(request, 'login.html', {'form': form})

def logout_v(request):
    request.session[settings.USER_SESSION_KEY] = {}

    return redirect("/login/")

from  utils.paper import Pagination
def hosts(request):

    #创建测试数据
    # for i in range(12):
    #     print("==start==>",i)
    #     models.Host.objects.create(
    #         hostname='abc%s.com'%i,
    #         ip='10.0.0.%s'%i,
    #         port=1521,
    #     )
    # return  HttpResponse("创建ok")

    all_count = models.Host.objects.all().count()
    page_obj = Pagination(request.GET.get('page'),all_count,request.path_info)
    # print(page_obj.start, page_obj.end,request.GET.get('page'))

    host_list=models.Host.objects.all().order_by('-id')[page_obj.start:page_obj.end]
    username = request.session[settings.USER_SESSION_KEY]['username']
    return  render(request,"host.html",{"page_html":page_obj.page_html,"host_list":host_list,"username":username})

def hosts_add(request):
    username = request.session[settings.USER_SESSION_KEY]['username']
    if request.method=='GET':
        form= HostModelsForm()
        return  render(request,"add_host.html",{"form":form})
    else:
        form=HostModelsForm(data=request.POST)
        if form.is_valid():
            # print( form.cleaned_data)
            obj=form.save()
            return  redirect("/hosts/")
    return  render(request,"add_host.html",{'form': form,"username":username})

def edit_host(request,nid):

    obj=models.Host.objects.filter(id=nid).first()
    username = request.session[settings.USER_SESSION_KEY]['username']
    if not obj:
        return  HttpResponse("主机不存在！")

    if request.method=="GET":
        print("nid:",nid)
        form=HostModelsForm(instance=obj)
        return render(request,"edit_host.html",{"form":form,"username":username })
    else:
        form=HostModelsForm(data=request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/hosts/")
        print("errors++>",form.errors)
        return render(request,"edit_host.html",{"form":form ,"username":username })

def delete_host(request,nid):
    obj = models.Host.objects.filter(id=nid).first()
    if not obj:
        return HttpResponse("主机不存在！")
    if request.method=="GET":
        models.Host.objects.filter(id=nid).delete()
        return redirect("/hosts/")

def users(request):
    all_count = models.UserInfo.objects.all().count()
    page_obj = Pagination(request.GET.get('page'), all_count, request.path_info)
    user_list = models.UserInfo.objects.all().order_by('-id')[page_obj.start:page_obj.end]
    username = request.session[settings.USER_SESSION_KEY]['username']
    return render(request, "users.html", {"page_html": page_obj.page_html, "user_list": user_list, "username": username})

def users_add(request):
    username = request.session[settings.USER_SESSION_KEY]['username']
    if request.method=='GET':
        form= UserInfoModelsForm()
        return  render(request,"add_user.html",{"form":form,"username":username})
    else:
        form=UserInfoModelsForm(data=request.POST)

        if form.is_valid():
            form.instance.password=md5(form.instance.password)
            obj=form.save()
            return  redirect("/users/")
    return  render(request,"add_user.html",{'form': form,"username":username})

def users_del(request,nid):
    obj = models.UserInfo.objects.filter(id=nid).first()
    if not obj:
        return HttpResponse("用户不存在！")
    if request.method == "GET":
        models.UserInfo.objects.filter(id=nid).delete()
        return redirect("/users/")

def users_edit(request,nid):
    obj = models.UserInfo.objects.filter(id=nid).first()
    username = request.session[settings.USER_SESSION_KEY]['username']
    if not obj:
        return HttpResponse("用户不存在！")

    if request.method == "GET":
        print("nid:", nid)
        form = UserInfoModelsForm(instance=obj)
        return render(request, "edit_user.html", {"form": form, "username": username})
    else:
        form = UserInfoModelsForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.instance.password = md5(form.instance.password)
            form.save()
            return redirect("/users/")
        return render(request, "edit_user.html", {"form": form, "username": username})

def test(request):
    # print(" pint=>test")
    return HttpResponse("OK")
    #方法一:
    # from django.core import serializers
    # quertset=models.Host.objects.filter(id__lt=5)
    # data=serializers.serialize("json",quertset)


    # 方法二：
    # import  json
    # host_list=models.Host.objects.filter(id__lt=5).values_list("hostname","ip","port")
    # data=json.dumps(list(host_list))
    # print(data)
    # return  HttpResponse(data)

    # 创建测试数据
    # for i in range(222):
    #     print("==start==>",i)
    #     models.Host.objects.create(
    #         hostname='abc%s.com'%i,
    #         ip='10.0.0.%s'%i,
    #         port=1521,
    #     )
    # return  HttpResponse("创建ok")













