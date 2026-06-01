# -*- coding: UTF-8 -*-
from django.db import models
from mirage import fields


class IDC(models.Model):
    """
    机房信息
    """
    idc_id = models.AutoField('机房ID', primary_key=True)
    idc_name = models.CharField('机房名称', max_length=100, unique=True)
    idc_code = models.CharField('机房编码', max_length=50, unique=True)
    idc_address = models.CharField('机房地址', max_length=255, blank=True)
    idc_contact = models.CharField('联系人', max_length=50, blank=True)
    idc_phone = models.CharField('联系电话', max_length=20, blank=True)
    idc_bandwidth = models.CharField('带宽信息', max_length=100, blank=True)
    idc_status = models.IntegerField('状态', choices=((0, '停用'), (1, '启用')), default=1)
    idc_remark = models.TextField('备注', blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.idc_name

    class Meta:
        managed = True
        db_table = 'resource_idc'
        verbose_name = u'机房信息'
        verbose_name_plural = u'机房信息'


class Server(models.Model):
    """
    服务器信息
    """
    server_id = models.AutoField('服务器ID', primary_key=True)
    server_name = models.CharField('服务器名称', max_length=100, unique=True)
    server_ip = models.CharField('服务器IP', max_length=100)
    server_inner_ip = models.CharField('内网IP', max_length=100, blank=True)
    server_port = models.IntegerField('SSH端口', default=22)
    server_username = models.CharField('SSH用户名', max_length=50, default='root')
    server_password = fields.EncryptedCharField(verbose_name='SSH密码', max_length=255, blank=True)
    idc = models.ForeignKey(IDC, verbose_name='所属机房', on_delete=models.CASCADE)
    server_cpu = models.CharField('CPU信息', max_length=255, blank=True)
    server_memory = models.CharField('内存信息', max_length=255, blank=True)
    server_disk = models.CharField('磁盘信息', max_length=255, blank=True)
    server_os = models.CharField('操作系统', max_length=100, blank=True)
    server_status = models.IntegerField('状态', choices=((0, '离线'), (1, '在线'), (2, '维护')), default=1)
    server_role = models.CharField('角色', max_length=50, blank=True)
    server_remark = models.TextField('备注', blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return f'{self.server_name}({self.server_ip})'

    class Meta:
        managed = True
        db_table = 'resource_server'
        verbose_name = u'服务器信息'
        verbose_name_plural = u'服务器信息'


class Project(models.Model):
    """
    项目信息
    """
    project_id = models.AutoField('项目ID', primary_key=True)
    project_name = models.CharField('项目名称', max_length=100, unique=True)
    project_code = models.CharField('项目编码', max_length=50, unique=True)
    project_owner = models.CharField('项目负责人', max_length=50, blank=True)
    project_owner_display = models.CharField('负责人中文名', max_length=50, blank=True)
    project_description = models.TextField('项目描述', blank=True)
    project_priority = models.IntegerField('优先级', choices=((1, '高'), (2, '中'), (3, '低')), default=2)
    project_status = models.IntegerField('状态', choices=((0, '停用'), (1, '启用')), default=1)
    project_remark = models.TextField('备注', blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.project_name

    class Meta:
        managed = True
        db_table = 'resource_project'
        verbose_name = u'项目信息'
        verbose_name_plural = u'项目信息'


class Cluster(models.Model):
    """
    集群信息
    """
    cluster_id = models.AutoField('集群ID', primary_key=True)
    cluster_name = models.CharField('集群名称', max_length=100, unique=True)
    cluster_code = models.CharField('集群编码', max_length=50, unique=True)
    project = models.ForeignKey(Project, verbose_name='所属项目', on_delete=models.CASCADE)
    cluster_type = models.CharField('集群类型', max_length=50, choices=(
        ('mysql', 'MySQL'), ('redis', 'Redis'), ('mongo', 'MongoDB'),
        ('pgsql', 'PostgreSQL'), ('oracle', 'Oracle'), ('other', '其他')
    ))
    cluster_role = models.CharField('集群角色', max_length=50, choices=(
        ('production', '生产环境'), ('test', '测试环境'), ('dev', '开发环境')
    ), default='production')
    servers = models.ManyToManyField(Server, verbose_name='包含服务器', blank=True)
    cluster_status = models.IntegerField('状态', choices=((0, '停用'), (1, '启用')), default=1)
    cluster_remark = models.TextField('备注', blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.cluster_name

    class Meta:
        managed = True
        db_table = 'resource_cluster'
        verbose_name = u'集群信息'
        verbose_name_plural = u'集群信息'


class ResourceInstance(models.Model):
    """
    实例资源关联 - 将现有Instance与资源管理模块关联
    """
    resource_instance_id = models.AutoField('关联ID', primary_key=True)
    instance_id = models.IntegerField('数据库实例ID')
    instance_name = models.CharField('实例名称', max_length=50)
    server = models.ForeignKey(Server, verbose_name='所属服务器', on_delete=models.CASCADE, null=True, blank=True)
    cluster = models.ForeignKey(Cluster, verbose_name='所属集群', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name='所属项目', on_delete=models.CASCADE, null=True, blank=True)
    idc = models.ForeignKey(IDC, verbose_name='所属机房', on_delete=models.CASCADE, null=True, blank=True)
    instance_env = models.CharField('环境类型', max_length=20, choices=(
        ('prod', '生产'), ('test', '测试'), ('dev', '开发')
    ), default='prod')
    instance_level = models.IntegerField('重要级别', choices=((1, '核心'), (2, '重要'), (3, '一般')), default=2)
    instance_remark = models.TextField('备注', blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return f'{self.instance_name} 资源关联'

    class Meta:
        managed = True
        db_table = 'resource_instance'
        verbose_name = u'实例资源关联'
        verbose_name_plural = u'实例资源关联'
