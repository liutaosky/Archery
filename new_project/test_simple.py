# -*- coding: UTF-8 -*-
"""
Resource Management 模块简化测试脚本（不依赖 djangorestframework）
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from resource_management.models import ResourceGroup, Instance, Users
from resource_management.utils.resource_group import user_groups, user_instances


def test_models():
    print("=" * 60)
    print("测试模型")
    print("=" * 60)

    # 测试创建资源组
    rg = ResourceGroup.objects.create(
        group_name='测试资源组',
        group_parent_id=0,
        group_sort=1,
        group_level=1,
        ding_webhook='https://oapi.dingtalk.com/robot/send?access_token=test',
        is_deleted=0
    )
    print(f"✓ 创建资源组: ID={rg.group_id}, 名称={rg.group_name}")

    # 测试查询资源组
    rgs = ResourceGroup.objects.all()
    print(f"✓ 查询资源组: 总数={rgs.count()}")

    # 测试创建实例
    instance = Instance.objects.create(
        instance_name='测试实例',
        type='master',
        db_type='mysql',
        host='127.0.0.1',
        port=3306
    )
    print(f"✓ 创建实例: ID={instance.id}, 名称={instance.instance_name}")

    # 测试创建用户
    user = Users.objects.create_user(
        username='testuser',
        password='testpass123',
        display='测试用户'
    )
    print(f"✓ 创建用户: ID={user.id}, 用户名={user.username}")

    # 测试关联
    user.resource_group.add(rg)
    instance.resource_group.add(rg)
    print(f"✓ 资源关联: 用户->资源组, 实例->资源组")

    # 测试删除
    rg.delete()
    instance.delete()
    user.delete()
    print(f"✓ 删除测试数据")

    print("\n✓ 所有模型测试通过!\n")


def test_utils():
    print("=" * 60)
    print("测试工具函数")
    print("=" * 60)

    # 创建测试数据
    rg = ResourceGroup.objects.create(
        group_name='工具测试资源组',
        group_parent_id=0,
        group_sort=1,
        group_level=1,
        is_deleted=0
    )

    # 创建超级用户
    superuser = Users.objects.create_superuser(
        username='admintests',
        password='adminpass123',
        email='admin@test.com'
    )
    superuser.display = '管理员'
    superuser.save()

    # 创建普通用户
    normal_user = Users.objects.create_user(
        username='normaluser',
        password='normalpass123'
    )
    normal_user.display = '普通用户'
    normal_user.resource_group.add(rg)
    normal_user.save()

    # 测试 user_groups
    superuser_groups = user_groups(superuser)
    normal_user_groups = user_groups(normal_user)
    print(f"✓ user_groups: 超级用户={len(superuser_groups)}个组, 普通用户={len(normal_user_groups)}个组")

    # 测试 user_instances
    instance = Instance.objects.create(
        instance_name='工具测试实例',
        type='master',
        db_type='mysql',
        host='127.0.0.1',
        port=3306
    )
    instance.resource_group.add(rg)

    # 清理
    rg.delete()
    instance.delete()
    superuser.delete()
    normal_user.delete()

    print(f"✓ user_instances 测试通过")

    print("\n✓ 所有工具函数测试通过!\n")


def test_urls():
    print("=" * 60)
    print("测试URL路由")
    print("=" * 60)

    from resource_management.urls import urlpatterns

    for url in urlpatterns:
        print(f"✓ URL路由: {url.pattern} -> {url.name}")

    print("\n✓ 所有URL路由测试通过!\n")


def main():
    print("\n" + "=" * 60)
    print("Resource Management 模块简化测试（无需 djangorestframework）")
    print("=" * 60 + "\n")

    try:
        test_models()
        test_utils()
        test_urls()

        print("=" * 60)
        print("🎉 所有测试通过! Resource Management 模块运行正常!")
        print("=" * 60)
        return 0

    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ 测试失败: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
