"""day24_myself URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^index/$', views.index),
    url(r'^login/$', views.login),
    url(r'^reg/$', views.reg),
    url(r'^logout_v/$', views.logout_v),
    url(r'^admin/', admin.site.urls),
    url(r'^hosts/$', views.hosts),
    url(r'^hosts/add/$', views.add),
    url(r'^hosts/edit/(\d+)/$', views.edit_host),
    url(r'^hosts/del/(\d+)/$', views.delete_host),

    url(r'^users/$', views.users),


    url(r'^test/$', views.test),
]
