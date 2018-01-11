# -*- coding: utf-8 -*-
__author__ = 'ShengLeQi'

from django import template
from django.utils.safestring import mark_safe

register = template.Library()  # register的名字是固定的,不可改变


@register.inclusion_tag("mytag.html")
def My_tag():
    Num="I am linux player!"
    return {"Num":Num}

@register.filter
def filter_multi(v1, v2):
    return v1 * v2


@register.filter
def filter_multi2(v1, v2,v3):
    return v1 * v2 * v3



@register.simple_tag
def simple_tag_multi(v1, v2):
    return v1 * v2


@register.simple_tag
def my_input(id, arg):
    result = "<input  type='text' id='%s' class='%s' />" % (id, arg,)
    return mark_safe(result)

@register.filter
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')