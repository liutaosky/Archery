# -*- coding: UTF-8 -*-
import logging
import traceback
import json
from itertools import chain

from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.db.models import F, Value, IntegerField
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('default')


def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return HttpResponse(json.dumps({'status': 1, 'msg': '无权限'}), content_type='application/json')
    return wrapper


@csrf_exempt
@superuser_required
def group(request):
    """获取资源组列表"""
    limit = int(request.POST.get('limit', 10))
    offset = int(request.POST.get('offset', 0))
    limit = offset + limit
    search = request.POST.get('search', '')

    group_obj = ResourceGroup.objects.filter(group_name__icontains=search, is_deleted=0)
    group_count = group_obj.count()
    group_list = group_obj[offset:limit].values("group_id", "group_name", "ding_webhook")

    rows = [row for row in group_list]

    result = {"total": group_count, "rows": rows}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def associated_objects(request):
    """
    获取资源组已关联对象信息
    type：(0, '用户'), (1, '实例')
    """
    group_id = int(request.POST.get('group_id'))
    object_type = request.POST.get('type')
    limit = int(request.POST.get('limit', 10))
    offset = int(request.POST.get('offset', 0))
    limit = offset + limit
    search = request.POST.get('search')

    resource_group = ResourceGroup.objects.get(group_id=group_id)
    rows_users = resource_group.users_set.all()
    rows_instances = resource_group.instance_set.all()

    if search:
        rows_users = rows_users.filter(display__contains=search)
        rows_instances = rows_instances.filter(instance_name__contains=search)

    rows_users = rows_users.annotate(
        object_id=F('id'),
        object_type=Value(0, output_field=IntegerField()),
        object_name=F('display'),
        group_id=F('resource_group__group_id'),
        group_name=F('resource_group__group_name')
    ).values('object_type', 'object_id', 'object_name', 'group_id', 'group_name')

    rows_instances = rows_instances.annotate(
        object_id=F('id'),
        object_type=Value(1, output_field=IntegerField()),
        object_name=F('instance_name'),
        group_id=F('resource_group__group_id'),
        group_name=F('resource_group__group_name')
    ).values('object_type', 'object_id', 'object_name', 'group_id', 'group_name')

    if object_type == '0':
        rows_obj = rows_users
        count = rows_obj.count()
        rows = [row for row in rows_obj][offset:limit]
    elif object_type == '1':
        rows_obj = rows_instances
        count = rows_obj.count()
        rows = [row for row in rows_obj][offset:limit]
    else:
        rows = list(chain(rows_users, rows_instances))
        count = len(rows)
        rows = rows[offset:limit]

    result = {'status': 0, 'msg': 'ok', "total": count, "rows": rows}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def unassociated_objects(request):
    """
    获取资源组未关联对象信息
    type：(0, '用户'), (1, '实例')
    """
    from resource_management.models import Users, Instance

    group_id = int(request.POST.get('group_id'))
    object_type = int(request.POST.get('object_type'))

    resource_group = ResourceGroup.objects.get(group_id=group_id)

    if object_type == 0:
        associated_user_ids = [user.id for user in resource_group.users_set.all()]
        rows = Users.objects.exclude(pk__in=associated_user_ids).annotate(
            object_id=F('pk'), object_name=F('display')).values('object_id', 'object_name')
    elif object_type == 1:
        associated_instance_ids = [ins.id for ins in resource_group.instance_set.all()]
        rows = Instance.objects.exclude(pk__in=associated_instance_ids).annotate(
            object_id=F('pk'), object_name=F('instance_name')
        ).values('object_id', 'object_name')
    else:
        raise ValueError('关联对象类型不正确')

    rows = [row for row in rows]
    result = {'status': 0, 'msg': 'ok', "rows": rows, "total": len(rows)}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def instances(request):
    """获取资源组关联实例列表"""
    group_name = request.POST.get('group_name')
    group_id = ResourceGroup.objects.get(group_name=group_name).group_id
    tag_code = request.POST.get('tag_code')
    db_type = request.POST.get('db_type')

    ins = ResourceGroup.objects.get(group_id=group_id).instance_set.all()

    filter_dict = dict()
    if db_type:
        filter_dict['db_type'] = db_type
    if tag_code:
        filter_dict['instance_tag__tag_code'] = tag_code
        filter_dict['instance_tag__active'] = True

    ins = ins.filter(**filter_dict).values('id', 'type', 'db_type', 'instance_name')
    rows = [row for row in ins]
    result = {'status': 0, 'msg': 'ok', "data": rows}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def user_all_instances(request):
    """获取用户所有实例列表（通过资源组间接关联）"""
    from resource_management.utils.resource_group import user_instances

    user = request.user
    type = request.GET.get('type')
    db_type = request.GET.getlist('db_type[]')
    tag_codes = request.GET.getlist('tag_codes[]')
    instances = user_instances(user, type, db_type, tag_codes).values('id', 'type', 'db_type', 'instance_name')
    rows = [row for row in instances]
    result = {'status': 0, 'msg': 'ok', "data": rows}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@superuser_required
def addrelation(request):
    """
    添加资源组关联对象
    type：(0, '用户'), (1, '实例')
    """
    from resource_management.models import Users, Instance

    group_id = int(request.POST.get('group_id'))
    object_type = request.POST.get('object_type')
    object_list = json.loads(request.POST.get('object_info'))

    try:
        resource_group = ResourceGroup.objects.get(group_id=group_id)
        obj_ids = [int(obj.split(',')[0]) for obj in object_list]

        if object_type == '0':
            resource_group.users_set.add(*Users.objects.filter(pk__in=obj_ids))
        elif object_type == '1':
            resource_group.instance_set.add(*Instance.objects.filter(pk__in=obj_ids))

        result = {'status': 0, 'msg': 'ok'}
    except Exception as e:
        logger.error(traceback.format_exc())
        result = {'status': 1, 'msg': str(e)}

    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def auditors(request):
    """获取资源组的审批流程"""
    group_name = request.POST.get('group_name')
    workflow_type = request.POST['workflow_type']
    result = {'status': 0, 'msg': 'ok', 'data': {'auditors': '', 'auditors_display': ''}}

    if group_name:
        group_id = ResourceGroup.objects.get(group_name=group_name).group_id
    else:
        result['status'] = 1
        result['msg'] = '参数错误'
        return HttpResponse(json.dumps(result), content_type='application/json')

    if audit_auth_groups:
        for auth_group_id in audit_auth_groups.split(','):
            try:
                Group.objects.get(id=auth_group_id)
            except Exception:
                result['status'] = 1
                result['msg'] = '审批流程权限组不存在，请重新配置！'
                return HttpResponse(json.dumps(result), content_type='application/json')

        audit_auth_groups_name = '->'.join(
            [Group.objects.get(id=auth_group_id).name for auth_group_id in audit_auth_groups.split(',')])
        result['data']['auditors'] = audit_auth_groups
        result['data']['auditors_display'] = audit_auth_groups_name

    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
@superuser_required
def changeauditors(request):
    """设置资源组的审批流程"""
    auth_groups = request.POST.get('audit_auth_groups')
    group_name = request.POST.get('group_name')
    workflow_type = request.POST.get('workflow_type')
    result = {'status': 0, 'msg': 'ok', 'data': []}

    group_id = ResourceGroup.objects.get(group_name=group_name).group_id
    audit_auth_groups = [str(Group.objects.get(name=auth_group).id) for auth_group in auth_groups.split(',')]

    try:
        pass
    except Exception as msg:
        logger.error(traceback.format_exc())
        result['msg'] = str(msg)
        result['status'] = 1

    return HttpResponse(json.dumps(result), content_type='application/json')
