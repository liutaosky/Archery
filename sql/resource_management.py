# -*- coding: UTF-8 -*-
"""
资源管理模块视图函数
"""
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from .models import IDC, Server, Project, Cluster, ResourceInstance, Instance
from sql.utils.resource_group import user_groups


@permission_required('sql.menu_idc', raise_exception=True)
def idc_list(request):
    """
    机房列表页面
    """
    # 关键字搜索
    keyword = request.GET.get('keyword', '')
    idc_query = IDC.objects.all()
    if keyword:
        idc_query = idc_query.filter(
            Q(idc_name__contains=keyword) |
            Q(idc_code__contains=keyword) |
            Q(idc_address__contains=keyword)
        )

    # 分页
    page = request.GET.get('page', 1)
    paginator = Paginator(idc_query.order_by('-create_time'), 10)
    idc_list = paginator.get_page(page)

    return render(request, 'resource/idc_list.html', {
        'idc_list': idc_list,
        'keyword': keyword,
    })


@permission_required('sql.menu_server', raise_exception=True)
def server_list(request):
    """
    服务器列表页面
    """
    # 获取用户所在资源组
    group_list = user_groups(request.user)
    group_ids = [group.group_id for group in group_list]

    # 关键字搜索
    keyword = request.GET.get('keyword', '')
    idc_id = request.GET.get('idc_id', '')

    server_query = Server.objects.all()
    # 如果不是管理员或没有查看所有资源权限，按资源组过滤
    if not (request.user.is_superuser or request.user.has_perm('sql.query_all_instances')):
        server_query = server_query.filter(resource_group__group_id__in=group_ids)

    if keyword:
        server_query = server_query.filter(
            Q(server_name__contains=keyword) |
            Q(server_ip__contains=keyword) |
            Q(server_inner_ip__contains=keyword)
        )
    if idc_id:
        server_query = server_query.filter(idc_id=idc_id)

    # 分页
    page = request.GET.get('page', 1)
    paginator = Paginator(server_query.order_by('-create_time').distinct(), 10)
    server_list = paginator.get_page(page)

    idc_list = IDC.objects.filter(idc_status=1)
    return render(request, 'resource/server_list.html', {
        'server_list': server_list,
        'idc_list': idc_list,
        'keyword': keyword,
        'idc_id': int(idc_id) if idc_id else '',
    })


@permission_required('sql.menu_project', raise_exception=True)
def project_list(request):
    """
    项目列表页面
    """
    # 获取用户所在资源组
    group_list = user_groups(request.user)
    group_ids = [group.group_id for group in group_list]

    # 关键字搜索
    keyword = request.GET.get('keyword', '')
    project_query = Project.objects.all()
    # 如果不是管理员，按资源组过滤
    if not request.user.is_superuser:
        project_query = project_query.filter(resource_group__group_id__in=group_ids)

    if keyword:
        project_query = project_query.filter(
            Q(project_name__contains=keyword) |
            Q(project_code__contains=keyword) |
            Q(project_owner__contains=keyword)
        )

    # 分页
    page = request.GET.get('page', 1)
    paginator = Paginator(project_query.order_by('-create_time').distinct(), 10)
    project_list = paginator.get_page(page)

    return render(request, 'resource/project_list.html', {
        'project_list': project_list,
        'keyword': keyword,
    })


@permission_required('sql.menu_cluster', raise_exception=True)
def cluster_list(request):
    """
    集群列表页面
    """
    # 关键字搜索
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

    # 分页
    page = request.GET.get('page', 1)
    paginator = Paginator(cluster_query.order_by('-create_time'), 10)
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


@permission_required('sql.resource_instance_view', raise_exception=True)
def resource_instance_list(request):
    """
    实例资源关联列表页面
    """
    # 关键字搜索
    keyword = request.GET.get('keyword', '')
    idc_id = request.GET.get('idc_id', '')
    project_id = request.GET.get('project_id', '')

    resource_instance_query = ResourceInstance.objects.all()

    if keyword:
        resource_instance_query = resource_instance_query.filter(
            Q(instance__instance_name__contains=keyword)
        )
    if idc_id:
        resource_instance_query = resource_instance_query.filter(idc_id=idc_id)
    if project_id:
        resource_instance_query = resource_instance_query.filter(project_id=project_id)

    # 分页
    page = request.GET.get('page', 1)
    paginator = Paginator(resource_instance_query.order_by('-create_time'), 10)
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


@permission_required('sql.resource_instance_edit', raise_exception=True)
def resource_instance_edit(request, resource_instance_id=None):
    """
    编辑实例资源关联
    """
    if resource_instance_id:
        resource_instance = get_object_or_404(ResourceInstance, resource_instance_id=resource_instance_id)
    else:
        resource_instance = None

    # 获取未被关联的实例
    linked_instance_ids = ResourceInstance.objects.values_list('instance_id', flat=True)
    if resource_instance:
        linked_instance_ids = linked_instance_ids.exclude(resource_instance_id=resource_instance_id)
    instance_list = Instance.objects.exclude(id__in=linked_instance_ids)
    
    # 如果是编辑状态，需要包含当前关联的实例
    if resource_instance:
        instance_list = list(instance_list) + [resource_instance.instance]

    if request.method == 'POST':
        # 处理表单提交
        instance_id = request.POST.get('instance')
        idc_id = request.POST.get('idc')
        server_id = request.POST.get('server')
        project_id = request.POST.get('project')
        cluster_id = request.POST.get('cluster')
        instance_env = request.POST.get('instance_env')
        instance_level = request.POST.get('instance_level')
        instance_remark = request.POST.get('instance_remark', '')

        if instance_id:
            if resource_instance:
                # 更新
                resource_instance.instance_id = instance_id
                resource_instance.idc_id = idc_id if idc_id else None
                resource_instance.server_id = server_id if server_id else None
                resource_instance.project_id = project_id if project_id else None
                resource_instance.cluster_id = cluster_id if cluster_id else None
                resource_instance.instance_env = instance_env
                resource_instance.instance_level = instance_level
                resource_instance.instance_remark = instance_remark
                resource_instance.save()
            else:
                # 创建
                ResourceInstance.objects.create(
                    instance_id=instance_id,
                    idc_id=idc_id if idc_id else None,
                    server_id=server_id if server_id else None,
                    project_id=project_id if project_id else None,
                    cluster_id=cluster_id if cluster_id else None,
                    instance_env=instance_env,
                    instance_level=instance_level,
                    instance_remark=instance_remark,
                )
            return redirect('resource_instance_list')

    # 渲染编辑页面
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
        'instance_list': instance_list,
    })
