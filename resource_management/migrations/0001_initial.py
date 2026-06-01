# -*- coding: UTF-8 -*-
from django.db import migrations, models
import mirage.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('idc_id', models.AutoField(primary_key=True, verbose_name='机房ID')),
                ('idc_name', models.CharField(max_length=100, unique=True, verbose_name='机房名称')),
                ('idc_code', models.CharField(max_length=50, unique=True, verbose_name='机房编码')),
                ('idc_address', models.CharField(blank=True, max_length=255, verbose_name='机房地址')),
                ('idc_contact', models.CharField(blank=True, max_length=50, verbose_name='联系人')),
                ('idc_phone', models.CharField(blank=True, max_length=20, verbose_name='联系电话')),
                ('idc_bandwidth', models.CharField(blank=True, max_length=100, verbose_name='带宽信息')),
                ('idc_status', models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=1, verbose_name='状态')),
                ('idc_remark', models.TextField(blank=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '机房信息',
                'verbose_name_plural': '机房信息',
                'db_table': 'resource_idc',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, verbose_name='项目ID')),
                ('project_name', models.CharField(max_length=100, unique=True, verbose_name='项目名称')),
                ('project_code', models.CharField(max_length=50, unique=True, verbose_name='项目编码')),
                ('project_owner', models.CharField(blank=True, max_length=50, verbose_name='项目负责人')),
                ('project_owner_display', models.CharField(blank=True, max_length=50, verbose_name='负责人中文名')),
                ('project_description', models.TextField(blank=True, verbose_name='项目描述')),
                ('project_priority', models.IntegerField(choices=[(1, '高'), (2, '中'), (3, '低')], default=2, verbose_name='优先级')),
                ('project_status', models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=1, verbose_name='状态')),
                ('project_remark', models.TextField(blank=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '项目信息',
                'verbose_name_plural': '项目信息',
                'db_table': 'resource_project',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('server_id', models.AutoField(primary_key=True, verbose_name='服务器ID')),
                ('server_name', models.CharField(max_length=100, unique=True, verbose_name='服务器名称')),
                ('server_ip', models.CharField(max_length=100, verbose_name='服务器IP')),
                ('server_inner_ip', models.CharField(blank=True, max_length=100, verbose_name='内网IP')),
                ('server_port', models.IntegerField(default=22, verbose_name='SSH端口')),
                ('server_username', models.CharField(default='root', max_length=50, verbose_name='SSH用户名')),
                ('server_password', mirage.fields.EncryptedCharField(blank=True, max_length=255, verbose_name='SSH密码')),
                ('server_cpu', models.CharField(blank=True, max_length=255, verbose_name='CPU信息')),
                ('server_memory', models.CharField(blank=True, max_length=255, verbose_name='内存信息')),
                ('server_disk', models.CharField(blank=True, max_length=255, verbose_name='磁盘信息')),
                ('server_os', models.CharField(blank=True, max_length=100, verbose_name='操作系统')),
                ('server_status', models.IntegerField(choices=[(0, '离线'), (1, '在线'), (2, '维护')], default=1, verbose_name='状态')),
                ('server_role', models.CharField(blank=True, max_length=50, verbose_name='角色')),
                ('server_remark', models.TextField(blank=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('idc', models.ForeignKey(on_delete=models.CASCADE, to='resource_management.idc', verbose_name='所属机房')),
            ],
            options={
                'verbose_name': '服务器信息',
                'verbose_name_plural': '服务器信息',
                'db_table': 'resource_server',
            },
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('cluster_id', models.AutoField(primary_key=True, verbose_name='集群ID')),
                ('cluster_name', models.CharField(max_length=100, unique=True, verbose_name='集群名称')),
                ('cluster_code', models.CharField(max_length=50, unique=True, verbose_name='集群编码')),
                ('cluster_type', models.CharField(choices=[('mysql', 'MySQL'), ('redis', 'Redis'), ('mongo', 'MongoDB'), ('pgsql', 'PostgreSQL'), ('oracle', 'Oracle'), ('other', '其他')], max_length=50, verbose_name='集群类型')),
                ('cluster_role', models.CharField(choices=[('production', '生产环境'), ('test', '测试环境'), ('dev', '开发环境')], default='production', max_length=50, verbose_name='集群角色')),
                ('cluster_status', models.IntegerField(choices=[(0, '停用'), (1, '启用')], default=1, verbose_name='状态')),
                ('cluster_remark', models.TextField(blank=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('project', models.ForeignKey(on_delete=models.CASCADE, to='resource_management.project', verbose_name='所属项目')),
                ('servers', models.ManyToManyField(blank=True, to='resource_management.server', verbose_name='包含服务器')),
            ],
            options={
                'verbose_name': '集群信息',
                'verbose_name_plural': '集群信息',
                'db_table': 'resource_cluster',
            },
        ),
        migrations.CreateModel(
            name='ResourceInstance',
            fields=[
                ('resource_instance_id', models.AutoField(primary_key=True, verbose_name='关联ID')),
                ('instance_id', models.IntegerField(verbose_name='数据库实例ID')),
                ('instance_name', models.CharField(max_length=50, verbose_name='实例名称')),
                ('instance_env', models.CharField(choices=[('prod', '生产'), ('test', '测试'), ('dev', '开发')], default='prod', max_length=20, verbose_name='环境类型')),
                ('instance_level', models.IntegerField(choices=[(1, '核心'), (2, '重要'), (3, '一般')], default=2, verbose_name='重要级别')),
                ('instance_remark', models.TextField(blank=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('cluster', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='resource_management.cluster', verbose_name='所属集群')),
                ('idc', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='resource_management.idc', verbose_name='所属机房')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='resource_management.project', verbose_name='所属项目')),
                ('server', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='resource_management.server', verbose_name='所属服务器')),
            ],
            options={
                'verbose_name': '实例资源关联',
                'verbose_name_plural': '实例资源关联',
                'db_table': 'resource_instance',
            },
        ),
    ]
