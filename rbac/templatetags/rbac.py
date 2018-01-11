import re
from django.template import Library
from django.conf import settings
register = Library()


"""
{% menu request %}
"""

@register.inclusion_tag('rbac/menu.html')
def menu(request):
    current_url = request.path_info
    # 获取session中菜单信息，自动生成二级菜单【默认选中，默认展开】
    permission_menu_list = request.session.get(settings.PERMISSION_MENU_SESSION_KEY)
    per_dict = {}
    for item in permission_menu_list:
        if not item['pid']:
            per_dict[item['id']] = item

    for item in permission_menu_list:
        reg = settings.REX_FORMAT % (item['url'])
        if not re.match(reg, current_url):
            continue
        # 匹配成功
        if item['pid']:
            per_dict[item['pid']]['active'] = True
        else:
            item['active'] = True

    """
    {
        1: {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1', 'active': True}, 
        5: {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu__name': '菜单1'}
        10: {'id': 10, 'title': 'xx列表', 'url': '/hosts/', 'pid': None, 'menu_id': 2, 'menu__name': '菜单2'}
    }

    {
        1:{
            'menu__name': '菜单1',
            'active': True,
            'children':[
                {'id': 1, 'title': '用户列表', 'url': '/users/','active': True}
                {'id': 5, 'title': '主机列表', 'url': '/users/'}
            ]
        },
        2:{
             'menu__name': '菜单1',
              'children':[
                {'id': 10, 'title': 'xx列表', 'url': '/hosts/'}
            ]

        }
    }
    """

    menu_result = {}
    for item in per_dict.values():
        menu_id = item['menu_id']
        if menu_id in menu_result:
            temp = {'id': item['id'], 'title': item['title'], 'url': item['url'], 'active': item.get('active', False)}
            menu_result[menu_id]['children'].append(temp)
            if item.get('active', False):
                menu_result[menu_id]['active'] = item.get('active', False)
        else:
            menu_result[menu_id] = {
                'menu__name': item['menu__name'],
                'active': item.get('active', False),
                'children': [
                    {'id': item['id'], 'title': item['title'], 'url': item['url'], 'active': item.get('active', False)}
                ]
            }
    return {'menu_result':menu_result}