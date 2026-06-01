# -*- coding: UTF-8 -*-
"""
资源管理模块视图函数
"""
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import IDC, Server, Project, Cluster, ResourceInstance
from .conf import get_page_size, is_permission_enabled


def permission_check(perm):
    """
    权限检查装饰器工厂
    根据配置决定是否启用权限检查
    """
    def decorator(view_func):
        if is_permission_enabled():
            return permission_required(perm, raise_exception=True)(view_func)
        return view_func
    return decorator


@permission_check('resource_management.view_idc')
def idc_list(request):
    """
    机房列表页面
    """
    keyword = request.GET.get('keyword', '')
    idc_query = IDC.objects.all()
    if keyword:
        idc_query = idc_query.filter(
            Q(idc_name__contains=keyword) |
            Q(idc_code__contains=keyword) |
            Q(idc_address__contains=keyword)
        )

    page = request.GET.get('page', 1)
    paginator = Paginator(idc_query.order_by('-create_time'), get_page_size())
    idc_list = paginator.get_page(page)

    return render(request, 'resource/idc_list.html', {
        'idc_list': idc_list,
        'keyword': keyword,
    })


@permission_check('resource_management.view_server')
def server_list(request):
    """
    服务器列表页面
    """
    keyword = request.GET.get('keyword', '')
    idc_id = request.GET.get('idc_id', '')

    server_query = Server.objects.all()

    if keyword:
        server_query = server_query.filter(
            Q(server_name__contains=keyword) |
            Q(server_ip__contains=keyword) |
            Q(server_inner_ip__contains=keyword)
        )
    if idc_id:
        server_query = server_query.filter(idc_id=idc_id)

    page = request.GET.get('page', 1)
    paginator = Paginator(server_query.order_by('-create_time').distinct(), get_page_size())
    server_list = paginator.get_page(page)

    idc_list = IDC.objects.filter(idc_status=1)
    return render(request, 'resource/server_list.html', {
        'server_list': server_list,
        'idc_list': idc_list,
        'keyword': keyword,
        'idc_id': int(idc_id) if idc_id else '',
    })


@permission_check('resource_management.view_project')
def project_list(request):
    """
    项目列表页面
    """
    keyword = request.GET.get('keyword', '')
    project_query = Project.objects.all()

    if keyword:
        project_query = project_query.filter(
            Q(project_name__contains=keyword) |
            Q(project_code__contains=keyword) |
            Q(project_owner__contains=keyword)
        )

    page = request.GET.get('page', 1)
    paginator = Paginator(project_query.order_by('-create_time').distinct(), get_page_size())
    project_list = paginator.get_page(page)

    return render(request, 'resource/project_list.html', {
        'project_list': project_list,
        'keyword': keyword,
    })


@permission_check('resource_management.view_cluster')
def cluster_list(request):
    """
    集群列表页面
    """
    keyword = request.GET.get('keyword', '')
    project_id = request.GET.get('project_id', '')
    cluster_type = request.GET.get('cluster_type', '')

    cluster_query = Cluster.objects.all()

    if keyword:
        cluster_query = cluster_query.filter(
            Q(cluster_name__contains=keyword) |
            Q(cluster_code__contains=keyword)
        )
    if project_id:
        cluster_query = cluster_query.filter(project_id=project_id)
    if cluster_type:
        cluster_query = cluster_query.filter(cluster_type=cluster_type)

    page = request.GET.get('page', 1)
    paginator = Paginator(cluster_query.order_by('-create_time'), get_page_size())
    cluster_list = paginator.get_page(page)

    project_list = Project.objects.filter(project_status=1)
    cluster_type_choices = [
        ('mysql', 'MySQL'), ('redis', 'Redis'), ('mongo', 'MongoDB'),
        ('pgsql', 'PostgreSQL'), ('oracle', 'Oracle'), ('other', '其他')
    ]

    return render(request, 'resource/cluster_list.html', {
        'cluster_list': cluster_list,
        'project_list': project_list,
        'cluster_type_choices': cluster_type_choices,
        'keyword': keyword,
        'project_id': int(project_id) if project_id else '',
        'cluster_type': cluster_type,
    })


@permission_check('resource_management.view_resourceinstance')
def resource_instance_list(request):
    """
    实例资源关联列表页面
    """
    keyword = request.GET.get('keyword', '')
    idc_id = request.GET.get('idc_id', '')
    project_id = request.GET.get('project_id', '')

    resource_instance_query = ResourceInstance.objects.all()

    if keyword:
        resource_instance_query = resource_instance_query.filter(
            Q(instance_name__contains=keyword)
        )
    if idc_id:
        resource_instance_query = resource_instance_query.filter(idc_id=idc_id)
    if project_id:
        resource_instance_query = resource_instance_query.filter(project_id=project_id)

    page = request.GET.get('page', 1)
    paginator = Paginator(resource_instance_query.order_by('-create_time'), get_page_size())
    resource_instance_list = paginator.get_page(page)

    idc_list = IDC.objects.filter(idc_status=1)
    project_list = Project.objects.filter(project_status=1)

    return render(request, 'resource/resource_instance_list.html', {
        'resource_instance_list': resource_instance_list,
        'idc_list': idc_list,
        'project_list': project_list,
        'keyword': keyword,
        'idc_id': int(idc_id) if idc_id else '',
        'project_id': int(project_id) if project_id else '',
    })


@permission_check('resource_management.change_resourceinstance')
def resource_instance_edit(request, resource_instance_id=None):
    """
    编辑实例资源关联
    """
    if resource_instance_id:
        resource_instance = get_object_or_404(ResourceInstance, resource_instance_id=resource_instance_id)
    else:
        resource_instance = None

    if request.method == 'POST':
        instance_id = request.POST.get('instance_id')
        instance_name = request.POST.get('instance_name')
        idc_id = request.POST.get('idc')
        server_id = request.POST.get('server')
        project_id = request.POST.get('project')
        cluster_id = request.POST.get('cluster')
        instance_env = request.POST.get('instance_env')
        instance_level = request.POST.get('instance_level')
        instance_remark = request.POST.get('instance_remark', '')

        if instance_id and instance_name:
            if resource_instance:
                resource_instance.instance_id = instance_id
                resource_instance.instance_name = instance_name
                resource_instance.idc_id = idc_id if idc_id else None
                resource_instance.server_id = server_id if server_id else None
                resource_instance.project_id = project_id if project_id else None
                resource_instance.cluster_id = cluster_id if cluster_id else None
                resource_instance.instance_env = instance_env
                resource_instance.instance_level = instance_level
                resource_instance.instance_remark = instance_remark
                resource_instance.save()
            else:
                ResourceInstance.objects.create(
                    instance_id=instance_id,
                    instance_name=instance_name,
                    idc_id=idc_id if idc_id else None,
                    server_id=server_id if server_id else None,
                    project_id=project_id if project_id else None,
                    cluster_id=cluster_id if cluster_id else None,
                    instance_env=instance_env,
                    instance_level=instance_level,
                    instance_remark=instance_remark,
                )
            return redirect('resource_instance_list')

    idc_list = IDC.objects.filter(idc_status=1)
    project_list = Project.objects.filter(project_status=1)
    server_list = Server.objects.filter(server_status=1)
    cluster_list = Cluster.objects.filter(cluster_status=1)

    return render(request, 'resource/resource_instance_edit.html', {
        'resource_instance': resource_instance,
        'idc_list': idc_list,
        'project_list': project_list,
        'server_list': server_list,
        'cluster_list': cluster_list,
    })


@permission_check('resource_management.delete_resourceinstance')
def resource_instance_delete(request, resource_instance_id):
    """
    删除实例资源关联
    """
    resource_instance = get_object_or_404(ResourceInstance, resource_instance_id=resource_instance_id)
    resource_instance.delete()
    return redirect('resource_instance_list')


def api_idc_list(request):
    """
    机房列表 API
    """
    keyword = request.GET.get('keyword', '')
    idc_query = IDC.objects.filter(idc_status=1)
    if keyword:
        idc_query = idc_query.filter(
            Q(idc_name__contains=keyword) |
            Q(idc_code__contains=keyword)
        )
    
    data = [{'id': item.idc_id, 'name': item.idc_name, 'code': item.idc_code} for item in idc_query]
    return JsonResponse({'status': 0, 'data': data})


def api_server_list(request):
    """
    服务器列表 API
    """
    idc_id = request.GET.get('idc_id', '')
    server_query = Server.objects.filter(server_status=1)
    if idc_id:
        server_query = server_query.filter(idc_id=idc_id)
    
    data = [{'id': item.server_id, 'name': item.server_name, 'ip': item.server_ip} for item in server_query]
    return JsonResponse({'status': 0, 'data': data})


def api_project_list(request):
    """
    项目列表 API
    """
    keyword = request.GET.get('keyword', '')
    project_query = Project.objects.filter(project_status=1)
    if keyword:
        project_query = project_query.filter(
            Q(project_name__contains=keyword) |
            Q(project_code__contains=keyword)
        )
    
    data = [{'id': item.project_id, 'name': item.project_name, 'code': item.project_code} for item in project_query]
    return JsonResponse({'status': 0, 'data': data})


def api_cluster_list(request):
    """
    集群列表 API
    """
    project_id = request.GET.get('project_id', '')
    cluster_query = Cluster.objects.filter(cluster_status=1)
    if project_id:
        cluster_query = cluster_query.filter(project_id=project_id)
    
    data = [{'id': item.cluster_id, 'name': item.cluster_name, 'type': item.cluster_type} for item in cluster_query]
    return JsonResponse({'status': 0, 'data': data})
