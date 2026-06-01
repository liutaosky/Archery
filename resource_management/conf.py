# -*- coding: UTF-8 -*-
"""
资源管理模块配置文件

该模块支持以下配置项：

RESOURCE_MANAGEMENT = {
    # 是否启用模块
    'ENABLED': True,
    
    # 是否启用权限控制
    'PERMISSION_ENABLED': True,
    
    # 默认每页显示数量
    'DEFAULT_PAGE_SIZE': 10,
    
    # 是否允许匿名访问（仅适用于只读视图）
    'ALLOW_ANONYMOUS': False,
    
    # 菜单配置
    'MENU': {
        'IDC': {'enabled': True, 'order': 1},
        'SERVER': {'enabled': True, 'order': 2},
        'PROJECT': {'enabled': True, 'order': 3},
        'CLUSTER': {'enabled': True, 'order': 4},
        'INSTANCE': {'enabled': True, 'order': 5},
    },
    
    # API配置
    'API': {
        'ENABLED': True,
        'VERSION': 'v1',
    }
}
"""

DEFAULT_CONFIG = {
    'ENABLED': True,
    'PERMISSION_ENABLED': True,
    'DEFAULT_PAGE_SIZE': 10,
    'ALLOW_ANONYMOUS': False,
    'MENU': {
        'IDC': {'enabled': True, 'order': 1},
        'SERVER': {'enabled': True, 'order': 2},
        'PROJECT': {'enabled': True, 'order': 3},
        'CLUSTER': {'enabled': True, 'order': 4},
        'INSTANCE': {'enabled': True, 'order': 5},
    },
    'API': {
        'ENABLED': True,
        'VERSION': 'v1',
    }
}


def get_config():
    """
    获取资源管理模块配置
    
    优先从 Django settings 中获取配置，若未配置则使用默认配置
    """
    from django.conf import settings
    
    return getattr(settings, 'RESOURCE_MANAGEMENT', DEFAULT_CONFIG)


def is_enabled():
    """
    检查模块是否启用
    """
    return get_config().get('ENABLED', True)


def is_permission_enabled():
    """
    检查权限控制是否启用
    """
    return get_config().get('PERMISSION_ENABLED', True)


def get_page_size():
    """
    获取默认每页显示数量
    """
    return get_config().get('DEFAULT_PAGE_SIZE', 10)
