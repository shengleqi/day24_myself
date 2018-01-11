from django.conf import settings

def init_permission(user,request):
    """
    用于做用户登录成功之后，权限信息的初始化。
    :param user: 登录的用户对象
    :param request: 请求相关的对象
    :return:
    """


    """
                [
                    {'permissions__title': '用户列表', 'permissions__url': '/users/', 'permissions__code': 'list', 'permissions__group_id': 1}
                    {'permissions__title': '添加用户', 'permissions__url': '/users/add/', 'permissions__code': 'add', 'permissions__group_id': 1}
                    {'permissions__title': '删除用户', 'permissions__url': '/users/del/(\\d+)/', 'permissions__code': 'del', 'permissions__group_id': 1}
                    {'permissions__title': '修改用户', 'permissions__url': '/users/edit/(\\d+)/', 'permissions__code': 'edit', 'permissions__group_id': 1}
                    {'permissions__title': '主机列表', 'permissions__url': '/hosts/', 'permissions__code': 'list', 'permissions__group_id': 2}
                    {'permissions__title': '添加主机', 'permissions__url': '/hosts/add/', 'permissions__code': 'add', 'permissions__group_id': 2}
                    {'permissions__title': '删除主机', 'permissions__url': '/hosts/del/(\\d+)/', 'permissions__code': 'del', 'permissions__group_id': 2}
                    {'permissions__title': '修改主机', 'permissions__url': '/hosts/edit/(\\d+)/', 'permissions__code': 'edit', 'permissions__group_id': 2}
                ]

                {
                    1(权限组ID): {
                        urls: [/u sers/,/users/add/ ,/users/del/(\d+)/],
                        codes: [list,add,del]
                    },
                    2: {
                        urls: [/hosts/,/hosts/add/ ,/hosts/del/(\d+)/],
                        codes: [list,add,del]
                    }
                }

                """
    permission_list = user.roles.filter(permissions__id__isnull=False).values(
        'permissions__id',    # 权限ID
        'permissions__title', # 权限名称
        'permissions__url',   # 权限URL
        'permissions__code',  # 权限CODE
        'permissions__group_menu_id',  # 组内菜单ID(null表示自己是菜单，1)
        'permissions__group_id', # 权限组ID
        'permissions__group__menu__id', # 一级菜单ID
        'permissions__group__menu__name', # 一级菜单名称
    ).distinct()

    # 获取权限信息+组+菜单，放入session，用于以后在页面上自动生成动态菜单。
    permission_memu_list = []
    for item in permission_list:
        val = {
            'id':item['permissions__id'],
            'title':item['permissions__title'],
            'url':item['permissions__url'],
            'pid':item['permissions__group_menu_id'],
            'menu_id':item['permissions__group__menu__id'],
            'menu__name':item['permissions__group__menu__name'],
        }
        permission_memu_list.append(val)
    request.session[settings.PERMISSION_MENU_SESSION_KEY] = permission_memu_list



    # 获取权限信息，放入session，用于以后在中间件中权限进行匹配
    permission_dict = {}
    for permission in permission_list:
        group_id = permission['permissions__group_id']
        url = permission['permissions__url']
        code = permission['permissions__code']
        if group_id in permission_dict:
            permission_dict[group_id]['urls'].append(url)
            permission_dict[group_id]['codes'].append(code)
        else:
            permission_dict[group_id] = {'urls': [url, ], 'codes': [code, ]}
    request.session[settings.PERMISSION_DICT_SESSION_KEY] = permission_dict




