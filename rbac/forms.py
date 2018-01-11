# -*- coding: utf-8 -*-
__author__ = 'ShengLeQi'
from  django.forms  import Form,ModelForm
from  django.forms import fields
from  django.forms import  widgets

from  rbac import  models
from  django import  forms
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError

class LoginForm(Form):
    username=fields.CharField(
        label="用户名",
        required=True,
        error_messages={
            'required':'用户名不能为空',
        },
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    password=fields.CharField(
        label='密码',
        required=True,
        error_messages={
            'required': '密码不能为空'
        },
        widget=widgets.PasswordInput(attrs={'class':'form-control'})

    )

class HostModelsForm(ModelForm):
    class Meta:
        model=models.Host
        fields=("hostname","ip","port","user","dp")
        widgets = {
            'hostname': widgets.TextInput(attrs={"class": "form-control"}),
            'ip': widgets.TextInput(attrs={"class": "form-control"}),
            'port': widgets.NumberInput(attrs={"class": "form-control"}),
            'user': widgets.SelectMultiple(attrs={"class": "form-control"}),
            'dp': widgets.SelectMultiple(attrs={"class": "form-control"}),
        }

        labels={
            "ip":"IP",
            "port":"端口",
        }
        error_messages={
            "ip":{
                "required":"IP不能为空",
            }
        }


class RegForm(Form):
    username=forms.CharField(label="用户名", min_length=3,
          widget=widgets.TextInput(attrs={"class": "form-control"})
                             )
    password=forms.CharField(label="密码", min_length=3,
          widget=widgets.PasswordInput(attrs={"class": "form-control"})
                             )
    re_password=forms.CharField(label="确认密码", min_length=3,
           widget=widgets.PasswordInput(attrs={"class": "form-control"})
                                    )
    email=forms.EmailField(label="邮箱", min_length=3,
           widget=widgets.TextInput(attrs={"class": "form-control"})
                            )

    def clean_username(self):

        return self.cleaned_data.get("username")

    def clean(self):
        if self.cleaned_data.get("password")==self.cleaned_data.get("re_password"):
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致")

class UserInfoModelsForm(ModelForm):
    class Meta:
        model=models.UserInfo
        fields=("username","password","roles")
        widgets = {
            'username': widgets.TextInput(attrs={"class": "form-control"}),
            'password': widgets.PasswordInput(attrs={"class": "form-control"}),
            'roles': widgets.SelectMultiple(attrs={"class": "form-control"}),
        }

        labels={
            "username":"用户名",
            "password":"密码",
            "roles":"角色",
        }
        error_messages={
            "ip":{
                "required":"IP不能为空",
            }
        }