# -*- coding: UTF-8 -*-
"""
资源管理模块自定义模板标签
"""
from django import template
from django.utils.safestring import mark_safe

from ..models import IDC, Server, Project, Cluster, ResourceInstance
from ..conf import get_config

register = template.Library()


@register.simple_tag
def get_resource_config(key, default=None):
    """
    获取资源管理模块配置项
    """
    config = get_config()
    return config.get(key, default)


@register.simple_tag
def resource_menu_items():
    """
    获取资源管理菜单配置
    """
    config = get_config()
    menu = config.get('MENU', {})
    items = []
    for key, value in menu.items():
        if value.get('enabled', True):
            items.append({
                'name': key,
                'url': f'/resource/{key.lower()}/',
                'order': value.get('order', 99)
            })
    return sorted(items, key=lambda x: x['order'])


@register.simple_tag
def idc_options(selected_id=None):
    """
    生成机房选择选项
    """
    idcs = IDC.objects.filter(idc_status=1)
    options = []
    for idc in idcs:
        selected = 'selected' if selected_id == idc.idc_id else ''
        options.append(f'<option value="{idc.idc_id}" {selected}>{idc.idc_name}</option>')
    return mark_safe('\n'.join(options))


@register.simple_tag
def server_options(selected_id=None, idc_id=None):
    """
    生成服务器选择选项
    """
    servers = Server.objects.filter(server_status=1)
    if idc_id:
        servers = servers.filter(idc_id=idc_id)
    options = []
    for server in servers:
        selected = 'selected' if selected_id == server.server_id else ''
        options.append(f'<option value="{server.server_id}" {selected}>{server.server_name} ({server.server_ip})</option>')
    return mark_safe('\n'.join(options))


@register.simple_tag
def project_options(selected_id=None):
    """
    生成项目选择选项
    """
    projects = Project.objects.filter(project_status=1)
    options = []
    for project in projects:
        selected = 'selected' if selected_id == project.project_id else ''
        options.append(f'<option value="{project.project_id}" {selected}>{project.project_name}</option>')
    return mark_safe('\n'.join(options))


@register.simple_tag
def cluster_options(selected_id=None, project_id=None):
    """
    生成集群选择选项
    """
    clusters = Cluster.objects.filter(cluster_status=1)
    if project_id:
        clusters = clusters.filter(project_id=project_id)
    options = []
    for cluster in clusters:
        selected = 'selected' if selected_id == cluster.cluster_id else ''
        options.append(f'<option value="{cluster.cluster_id}" {selected}>{cluster.cluster_name}</option>')
    return mark_safe('\n'.join(options))
