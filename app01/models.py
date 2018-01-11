from django.db import models

# class UserInfo(models.Model):
#     # nid = models.AutoField(primary_key=True)
#     # nid = models.BigAutoField(primary_key=True)
#     username = models.CharField(max_length=32)
#     password = models.CharField(max_length=64)
#     email = models.EmailField()
#
#     role=models.ForeignKey(to="Role",default=2)
#
#     def __str__(self):
#         return self.username
#
# class Department(models.Model):
#     title = models.CharField(max_length=32)
#
#     def __str__(self):
#         return self.title
#
# class Host(models.Model):
#     hostname = models.CharField(verbose_name='主机名', max_length=32)
#     ip = models.CharField(verbose_name='IP',max_length=32)# ip = models.GenericIPAddressField(protocol='both')
#     port = models.IntegerField(verbose_name="端口")
#     user = models.ForeignKey(verbose_name="用户名",to='UserInfo',default=1)
#     dp = models.ManyToManyField(verbose_name="部门",to="Department")
#
# class Role(models.Model):
#     id= models.AutoField(auto_created=True, primary_key=True)
#     rolename=models.CharField(max_length=32)
