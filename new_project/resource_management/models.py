# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


class ResourceGroup(models.Model):
    """
    资源组
    """
    group_id = models.AutoField('组ID', primary_key=True)
    group_name = models.CharField('组名称', max_length=100, unique=True)
    group_parent_id = models.BigIntegerField('父级id', default=0)
    group_sort = models.IntegerField('排序', default=1)
    group_level = models.IntegerField('层级', default=1)
    ding_webhook = models.CharField('钉钉webhook地址', max_length=255, blank=True)
    feishu_webhook = models.CharField('飞书webhook地址', max_length=255, blank=True)
    qywx_webhook = models.CharField('企业微信webhook地址', max_length=255, blank=True)
    is_deleted = models.IntegerField('是否删除', choices=((0, '否'), (1, '是')), default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    sys_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

    class Meta:
        managed = True
        db_table = 'resource_group'
        verbose_name = '资源组管理'
        verbose_name_plural = '资源组管理'


class Users(AbstractUser):
    """
    用户信息扩展
    """
    display = models.CharField('显示的中文名', max_length=50, default='')
    ding_user_id = models.CharField('钉钉UserID', max_length=64, blank=True)
    wx_user_id = models.CharField('企业微信UserID', max_length=64, blank=True)
    feishu_open_id = models.CharField('飞书OpenID', max_length=64, blank=True)
    failed_login_count = models.IntegerField('失败计数', default=0)
    last_login_failed_at = models.DateTimeField('上次失败登录时间', blank=True, null=True)
    resource_group = models.ManyToManyField(ResourceGroup, verbose_name='资源组', blank=True)

    def save(self, *args, **kwargs):
        self.failed_login_count = min(127, self.failed_login_count)
        self.failed_login_count = max(0, self.failed_login_count)
        super(Users, self).save(*args, **kwargs)

    def __str__(self):
        if self.display:
            return self.display
        return self.username

    class Meta:
        managed = True
        db_table = 'sql_users'
        verbose_name = '用户管理'
        verbose_name_plural = '用户管理'


class Instance(models.Model):
    """
    数据库实例配置
    """
    DB_TYPE_CHOICES = (
        ('mysql', 'MySQL'),
        ('mssql', 'MsSQL'),
        ('redis', 'Redis'),
        ('pgsql', 'PgSQL'),
        ('oracle', 'Oracle'),
        ('mongo', 'Mongo'),
        ('phoenix', 'Phoenix'),
        ('odps', 'ODPS'),
        ('clickhouse', 'ClickHouse'),
    )
    TYPE_CHOICES = (
        ('master', '主库'),
        ('slave', '从库'),
    )
    instance_name = models.CharField('实例名称', max_length=50, unique=True)
    type = models.CharField('实例类型', max_length=6, choices=TYPE_CHOICES)
    db_type = models.CharField('数据库类型', max_length=20, choices=DB_TYPE_CHOICES)
    host = models.CharField('实例连接', max_length=200)
    port = models.IntegerField('端口', default=0)
    resource_group = models.ManyToManyField(ResourceGroup, verbose_name='资源组', blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.instance_name

    class Meta:
        managed = True
        db_table = 'sql_instance'
        verbose_name = '实例配置'
        verbose_name_plural = '实例配置'
