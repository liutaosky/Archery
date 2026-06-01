# -*- coding: UTF-8 -*-
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ResourceManagementConfig(AppConfig):
    """
    资源管理模块应用配置
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resource_management'
    verbose_name = _('资源管理')

    def ready(self):
        """
        应用启动时的初始化操作
        """
        from . import signals
