# -*- coding: UTF-8 -*-
"""
资源管理模块信号处理
"""
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


@receiver(post_migrate)
def create_resource_permissions(sender, **kwargs):
    """
    在数据库迁移后创建资源管理相关权限
    """
    if sender.name == 'resource_management':
        from .models import IDC, Server, Project, Cluster, ResourceInstance
        
        models = [IDC, Server, Project, Cluster, ResourceInstance]
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            
            permissions = [
                (f'view_{model.__name__.lower()}', f'查看{model._meta.verbose_name}'),
                (f'add_{model.__name__.lower()}', f'添加{model._meta.verbose_name}'),
                (f'change_{model.__name__.lower()}', f'修改{model._meta.verbose_name}'),
                (f'delete_{model.__name__.lower()}', f'删除{model._meta.verbose_name}'),
            ]
            
            for codename, name in permissions:
                Permission.objects.get_or_create(
                    codename=codename,
                    content_type=content_type,
                    defaults={'name': name}
                )
