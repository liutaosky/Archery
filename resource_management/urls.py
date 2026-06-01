# -*- coding: UTF-8 -*-
"""
资源管理模块 URL 配置

使用方法：
在项目的 urls.py 中包含此模块：

    urlpatterns = [
        ...
        path('resource/', include('resource_management.urls')),
        ...
    ]

或使用命名空间：

    urlpatterns = [
        ...
        path('resource/', include(('resource_management.urls', 'resource_management'), namespace='resource')),
        ...
    ]

URL 列表：
- /resource/idc/ - 机房列表
- /resource/server/ - 服务器列表
- /resource/project/ - 项目列表
- /resource/cluster/ - 集群列表
- /resource/instance/ - 实例资源关联列表
- /resource/instance/edit/<int:resource_instance_id>/ - 编辑实例资源关联
- /resource/instance/add/ - 添加实例资源关联
- /resource/instance/delete/<int:resource_instance_id>/ - 删除实例资源关联

API 接口：
- /resource/api/idc/ - 机房列表 API
- /resource/api/server/ - 服务器列表 API
- /resource/api/project/ - 项目列表 API
- /resource/api/cluster/ - 集群列表 API
"""

from django.urls import path

from .views import (
    idc_list,
    server_list,
    project_list,
    cluster_list,
    resource_instance_list,
    resource_instance_edit,
    resource_instance_delete,
    api_idc_list,
    api_server_list,
    api_project_list,
    api_cluster_list,
)

app_name = 'resource_management'

urlpatterns = [
    # 机房管理
    path('idc/', idc_list, name='idc_list'),
    
    # 服务器管理
    path('server/', server_list, name='server_list'),
    
    # 项目管理
    path('project/', project_list, name='project_list'),
    
    # 集群管理
    path('cluster/', cluster_list, name='cluster_list'),
    
    # 实例资源关联管理
    path('instance/', resource_instance_list, name='resource_instance_list'),
    path('instance/edit/<int:resource_instance_id>/', resource_instance_edit, name='resource_instance_edit'),
    path('instance/add/', resource_instance_edit, name='resource_instance_add'),
    path('instance/delete/<int:resource_instance_id>/', resource_instance_delete, name='resource_instance_delete'),
    
    # API 接口
    path('api/idc/', api_idc_list, name='api_idc_list'),
    path('api/server/', api_server_list, name='api_server_list'),
    path('api/project/', api_project_list, name='api_project_list'),
    path('api/cluster/', api_cluster_list, name='api_cluster_list'),
]
