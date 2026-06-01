# -*- coding: UTF-8 -*-
"""
资源管理模块注册工具

提供模块注册和集成的便捷方法
"""
from django.apps import apps
from django.urls import path, include


def register_resource_management():
    """
    注册资源管理模块
    
    在 Django 项目中注册资源管理模块的所有组件
    """
    from django.conf import settings
    
    if 'resource_management' not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS = list(settings.INSTALLED_APPS) + ['resource_management']
    
    return True


def get_urls():
    """
    获取资源管理模块的 URL 配置
    
    可以在项目的 urls.py 中使用：
    urlpatterns += resource_management.get_urls()
    """
    from . import urls
    
    return [
        path('resource/', include('resource_management.urls')),
    ]


def get_menu_items():
    """
    获取资源管理模块的菜单项配置
    
    返回格式：
    [
        {'name': 'IDC', 'url': '/resource/idc/', 'label': '机房信息'},
        ...
    ]
    """
    from .conf import get_config
    
    config = get_config()
    menu_config = config.get('MENU', {})
    
    menu_items = [
        {'key': 'IDC', 'label': '机房信息', 'url': '/resource/idc/'},
        {'key': 'SERVER', 'label': '服务器信息', 'url': '/resource/server/'},
        {'key': 'PROJECT', 'label': '项目信息', 'url': '/resource/project/'},
        {'key': 'CLUSTER', 'label': '集群信息', 'url': '/resource/cluster/'},
        {'key': 'INSTANCE', 'label': '实例信息', 'url': '/resource/instance/'},
    ]
    
    enabled_items = []
    for item in menu_items:
        key = item['key']
        if key in menu_config and menu_config[key].get('enabled', True):
            item['order'] = menu_config[key].get('order', 99)
            enabled_items.append(item)
    
    return sorted(enabled_items, key=lambda x: x['order'])


def is_installed():
    """
    检查资源管理模块是否已安装
    """
    return apps.is_installed('resource_management')


def uninstall_resource_management():
    """
    卸载资源管理模块
    
    从 Django 配置中移除资源管理模块
    """
    from django.conf import settings
    
    if 'resource_management' in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS = [app for app in settings.INSTALLED_APPS if app != 'resource_management']
    
    return True


def get_permissions():
    """
    获取资源管理模块的所有权限列表
    """
    permissions = [
        ('resource_management.view_idc', '查看机房信息'),
        ('resource_management.add_idc', '添加机房信息'),
        ('resource_management.change_idc', '修改机房信息'),
        ('resource_management.delete_idc', '删除机房信息'),
        
        ('resource_management.view_server', '查看服务器信息'),
        ('resource_management.add_server', '添加服务器信息'),
        ('resource_management.change_server', '修改服务器信息'),
        ('resource_management.delete_server', '删除服务器信息'),
        
        ('resource_management.view_project', '查看项目信息'),
        ('resource_management.add_project', '添加项目信息'),
        ('resource_management.change_project', '修改项目信息'),
        ('resource_management.delete_project', '删除项目信息'),
        
        ('resource_management.view_cluster', '查看集群信息'),
        ('resource_management.add_cluster', '添加集群信息'),
        ('resource_management.change_cluster', '修改集群信息'),
        ('resource_management.delete_cluster', '删除集群信息'),
        
        ('resource_management.view_resourceinstance', '查看实例资源关联'),
        ('resource_management.add_resourceinstance', '添加实例资源关联'),
        ('resource_management.change_resourceinstance', '修改实例资源关联'),
        ('resource_management.delete_resourceinstance', '删除实例资源关联'),
    ]
    
    return permissions
