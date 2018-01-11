from django.db import models

class UserInfo(models.Model):
    """
    用户表
        1      alex        123
        2      tianle      123
        2      yanglei      123

    """
    username = models.CharField(verbose_name='用户名',max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)

    roles = models.ManyToManyField(verbose_name='拥有角色',to="Role")

    def __str__(self):
        return  self.username

class Role(models.Model):
    """
    角色表
        1    CEO
        2    CTO
        3    UFO
        4    销售主管
        5    销售员
    """
    title = models.CharField(verbose_name='角色名称',max_length=32)

    permissions = models.ManyToManyField(verbose_name='拥有权限',to="Permission")

    def __str__(self):
        return self.title

class Menu(models.Model):
    """
    菜单表
        菜单1：
            用户权限组
                用户列表
            主机权限组
                主机列表
    """
    name = models.CharField(max_length=32)

    def __str__(self):
        return  self.name

class PermissionGroup(models.Model):
    """
    权限组
        1    用户权限组
                用户列表
        2    主机权限组
                主机列表
    """
    caption = models.CharField(max_length=32)
    menu = models.ForeignKey(verbose_name='所属菜单',to='Menu')

class Permission(models.Model):
    """
    权限表
                                                                                组内菜单ID
        1     用户列表      /users/                 list               1            null
        2     添加用户      /users/add/             add                1            1
        3     删除用户      /users/del/(\d+)/       del                1            1
        4     修改用户      /users/edit/(\d+)/      edit               1            1

        5     主机列表      /hosts/                 list               2            null
        6     添加主机      /hosts/add/             add                2             5
        7     删除主机      /hosts/del/(\d+)/       del                2             5
        8     修改主机      /hosts/edit/(\d+)/      edit               2             5

    以后获取当前用户权限后，数据结构化处理，并放入session
    {
        1: {
            urls: [/users/,/users/add/ ,/users/del/(\d+)/],
            codes: [list,add,del]
        },
        2: {
            urls: [/hosts/,/hosts/add/ ,/hosts/del/(\d+)/],
            codes: [list,add,del]
        }
    }


    """
    title = models.CharField(verbose_name='权限名称',max_length=32)
    url = models.CharField(verbose_name='含正则的URL',max_length=255)
    code = models.CharField(verbose_name="权限代码",max_length=32)
    group = models.ForeignKey(verbose_name='所属权限组',to="PermissionGroup")
    # is_menu = models.BooleanField(verbose_name='是否是菜单')
    group_menu = models.ForeignKey(verbose_name='组内菜单',to="Permission",null=True,blank=True,related_name='xxx')

class Department(models.Model):
    '''
    部门
    '''
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

class Host(models.Model):
    '''
    主机相关信息
    '''
    hostname = models.CharField(verbose_name='主机名', max_length=32)
    ip = models.CharField(verbose_name='IP',max_length=32)# ip = models.GenericIPAddressField(protocol='both')
    port = models.IntegerField(verbose_name="端口")
    user = models.ManyToManyField(verbose_name="用户名",to='UserInfo',default=1)
    dp = models.ManyToManyField(verbose_name="部门",to="Department")

    def __str__(self):
        return  self.hostname



