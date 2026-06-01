# -*- coding: UTF-8 -*-
"""
资源管理模块 - 可插拔的 Django 应用

该模块提供完整的资源管理功能，包括：
- 机房信息管理
- 服务器信息管理
- 项目信息管理
- 集群信息管理
- 实例资源关联管理

模块特性：
- 松耦合设计，易于集成和移除
- 支持配置化注册
- 提供清晰的API接口
- 完整的权限控制
"""

__version__ = '1.0.0'
__author__ = 'Archery Team'

default_app_config = 'resource_management.apps.ResourceManagementConfig'
