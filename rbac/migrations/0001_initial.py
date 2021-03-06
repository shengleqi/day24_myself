# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-09 06:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32, verbose_name='主机名')),
                ('ip', models.CharField(max_length=32, verbose_name='IP')),
                ('port', models.IntegerField(verbose_name='端口')),
                ('dp', models.ManyToManyField(to='rbac.Department', verbose_name='部门')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='权限名称')),
                ('url', models.CharField(max_length=255, verbose_name='含正则的URL')),
                ('code', models.CharField(max_length=32, verbose_name='权限代码')),
            ],
        ),
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='所属菜单')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='角色名称')),
                ('permissions', models.ManyToManyField(to='rbac.Permission', verbose_name='拥有权限')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('roles', models.ManyToManyField(to='rbac.Role', verbose_name='拥有角色')),
            ],
        ),
        migrations.AddField(
            model_name='permission',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.PermissionGroup', verbose_name='所属权限组'),
        ),
        migrations.AddField(
            model_name='permission',
            name='group_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='xxx', to='rbac.Permission', verbose_name='组内菜单'),
        ),
        migrations.AddField(
            model_name='host',
            name='user',
            field=models.ManyToManyField(default=1, to='rbac.UserInfo', verbose_name='用户名'),
        ),
    ]
