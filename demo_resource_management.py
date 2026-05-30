#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
资源管理模块演示脚本
展示已实现的资源管理功能
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quick_settings")
django.setup()

from django.utils import timezone
from sql.models import IDC, Server, Project, Cluster, ResourceInstance, Instance, Users, ResourceGroup


def print_section(title):
    """打印章节标题"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def demo_data_model():
    """演示数据模型"""
    print_section("1. 资源管理数据模型")
    
    print("✅ 机房信息模型 (IDC):")
    print(f"   字段: idc_id, idc_name, idc_code, idc_address, idc_contact,")
    print(f"         idc_phone, idc_bandwidth, idc_status, idc_remark")
    
    print("\n✅ 服务器信息模型 (Server):")
    print(f"   字段: server_id, server_name, server_ip, server_inner_ip,")
    print(f"         server_port, server_username, server_password, idc,")
    print(f"         server_cpu, server_memory, server_disk, server_os,")
    print(f"         server_status, server_role, resource_group")
    
    print("\n✅ 项目信息模型 (Project):")
    print(f"   字段: project_id, project_name, project_code, project_owner,")
    print(f"         project_owner_display, project_description, project_priority,")
    print(f"         project_status, resource_group")
    
    print("\n✅ 集群信息模型 (Cluster):")
    print(f"   字段: cluster_id, cluster_name, cluster_code, project, cluster_type,")
    print(f"         cluster_role, servers, cluster_status")
    
    print("\n✅ 实例资源关联模型 (ResourceInstance):")
    print(f"   字段: resource_instance_id, instance, server, cluster, project,")
    print(f"         idc, instance_env, instance_level, instance_remark")


def demo_file_structure():
    """演示文件结构"""
    print_section("2. 已创建的文件结构")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("📁 sql/templates/resource/")
    templates_dir = os.path.join(base_dir, "sql", "templates", "resource")
    for f in sorted(os.listdir(templates_dir)):
        print(f"   - {f}")
    
    print("\n📁 sql/")
    print("   - models.py (已添加资源管理模型)")
    print("   - admin.py (已添加资源管理Admin配置)")
    print("   - resource_management.py (已添加视图函数)")
    print("   - urls.py (已添加资源管理URL路由)")
    
    print("\n📁 common/templates/")
    print("   - base.html (已添加资源管理菜单项)")
    
    print("\n📁 src/init_sql/")
    print("   - v2.0.0_resource_management.sql (数据库迁移SQL)")


def demo_relationships():
    """演示实体关系"""
    print_section("3. 资源管理实体关系")
    
    print("🏗️  关系图:")
    print()
    print("     IDC (机房)")
    print("      ↑")
    print("      |")
    print("   Server (服务器) ←→ ResourceGroup (资源组)")
    print("      ↑")
    print("      |")
    print("   Cluster (集群) ←→ Project (项目)")
    print("      ↓")
    print("      |")
    print("ResourceInstance ←→ Instance (数据库实例)")
    print("")
    print("📋 详细关系:")
    print("   - Server.idc → IDC (多对一)")
    print("   - Server.resource_group → ResourceGroup (多对多)")
    print("   - Cluster.project → Project (多对一)")
    print("   - Cluster.servers → Server (多对多)")
    print("   - ResourceInstance.instance → Instance (一对一)")
    print("   - ResourceInstance.server → Server (多对一，可选)")
    print("   - ResourceInstance.cluster → Cluster (多对一，可选)")
    print("   - ResourceInstance.project → Project (多对一，可选)")
    print("   - ResourceInstance.idc → IDC (多对一，可选)")


def demo_admin_config():
    """演示Admin配置"""
    print_section("4. Django Admin 后台配置")
    
    print("✅ 已注册的管理模块:")
    print("   - IDCAdmin: 机房信息管理")
    print("   - ServerAdmin: 服务器信息管理")
    print("   - ProjectAdmin: 项目信息管理")
    print("   - ClusterAdmin: 集群信息管理")
    print("   - ResourceInstanceAdmin: 实例资源关联管理")
    
    print("\n🎨 Admin功能特性:")
    print("   - 列表显示（list_display）")
    print("   - 搜索功能（search_fields）")
    print("   - 过滤功能（list_filter）")
    print("   - 多对多关系编辑（filter_horizontal）")


def demo_views():
    """演示视图函数"""
    print_section("5. 视图函数")
    
    print("🌐 已实现的视图:")
    print("   - idc_list: 机房列表页面")
    print("   - server_list: 服务器列表页面")
    print("   - project_list: 项目列表页面")
    print("   - cluster_list: 集群列表页面")
    print("   - resource_instance_list: 实例资源关联列表")
    print("   - resource_instance_edit: 编辑实例资源关联")
    
    print("\n🔒 权限控制:")
    print("   - 使用 @permission_required 装饰器")
    print("   - 按资源组过滤数据")


def demo_urls():
    """演示URL配置"""
    print_section("6. URL 路由配置")
    
    print("🔗 资源管理模块路由:")
    print("   /resource/idc/ → 机房管理")
    print("   /resource/server/ → 服务器管理")
    print("   /resource/project/ → 项目管理")
    print("   /resource/cluster/ → 集群管理")
    print("   /resource/instance/ → 实例资源关联")
    print("   /resource/instance/add/ → 添加实例关联")
    print("   /resource/instance/edit/<id>/ → 编辑实例关联")


def demo_templates():
    """演示模板文件"""
    print_section("7. 前端模板文件")
    
    templates = [
        ("idc_list.html", "机房列表页面"),
        ("server_list.html", "服务器列表页面"), 
        ("project_list.html", "项目列表页面"),
        ("cluster_list.html", "集群列表页面"),
        ("resource_instance_list.html", "实例资源关联列表"),
        ("resource_instance_edit.html", "实例资源关联编辑页面"),
    ]
    
    for file, desc in templates:
        print(f"📄 {file} - {desc}")
    
    print("\n🎨 模板特性:")
    print("   - 继承 base.html 统一布局")
    print("   - 搜索框功能")
    print("   - 数据表格展示")
    print("   - 分页功能")
    print("   - 筛选功能")


def demo_menu_integration():
    """演示菜单集成"""
    print_section("8. 导航菜单集成")
    
    print("🧭 已在 base.html 中添加:")
    print("   - 资源管理主菜单")
    print("   - 机房管理子菜单")
    print("   - 服务器管理子菜单")
    print("   - 项目管理子菜单")
    print("   - 集群管理子菜单")
    print("   - 实例关联子菜单")
    
    print("\n🔐 权限控制:")
    print("   - 菜单显示基于用户权限")
    print("   - 使用 {% if perms.sql.menu_xxx %} 标签")


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 20 + "资源管理模块演示" + " " * 24 + "║")
    print("╚" + "═" * 58 + "╝")
    
    demo_data_model()
    demo_file_structure()
    demo_relationships()
    demo_admin_config()
    demo_views()
    demo_urls()
    demo_templates()
    demo_menu_integration()
    
    print_section("9. 部署说明")
    print("📋 完整部署步骤:")
    print("   1. 执行 src/init_sql/v2.0.0_resource_management.sql")
    print("   2. 运行 python manage.py migrate")
    print("   3. 在 Django Admin 中为用户分配资源管理权限")
    print("   4. 启动服务访问资源管理菜单")
    
    print("\n" + "=" * 60)
    print("✅ 资源管理模块开发完成！")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
