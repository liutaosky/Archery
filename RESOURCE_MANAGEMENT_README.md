# 资源管理模块文档

## 📋 概述

资源管理模块是 Archery SQL 平台的新增企业级资源管理功能，提供机房、服务器、项目、集群和实例的完整生命周期管理。

## 🗂️ 模块结构

### 数据模型

- **IDC** - 机房信息管理
- **Server** - 服务器信息管理
- **Project** - 项目信息管理
- **Cluster** - 集群信息管理
- **ResourceInstance** - 实例资源关联

### 核心文件清单

| 文件路径 | 说明 |
|---------|------|
| [sql/models.py](file:///workspace/sql/models.py#L924-L1066] | 数据模型定义 |
| [sql/admin.py](file:///workspace/sql/admin.py#L268-L315) | Django Admin 配置 |
| [sql/resource_management.py](file:///workspace/sql/resource_management.py) | 视图函数 |
| [sql/urls.py](file:///workspace/sql/urls.py#L167-L173) | URL 路由配置 |
| [common/templates/base.html](file:///workspace/common/templates/base.html) | 导航菜单集成 |
| [sql/templates/resource/*.html](file:///workspace/sql/templates/resource) | 前端模板文件 |
| [src/init_sql/v2.0.0_resource_management.sql](file:///workspace/src/init_sql/v2.0.0_resource_management.sql) | 数据库迁移SQL |

## 🏗️ 实体关系图

```
     IDC (机房)
      ↑
      |
   Server (服务器) ←→ ResourceGroup (资源组)
      ↑
      |
   Cluster (集群) ←→ Project (项目)
      ↓
      |
ResourceInstance ←→ Instance (数据库实例)
```

## 📊 详细关系

- **Server.idc → IDC** (多对一)
- **Server.resource_group → ResourceGroup** (多对多)
- **Cluster.project → Project** (多对一)
- **Cluster.servers → Server** (多对多)
- **ResourceInstance.instance → Instance** (一对一)
- **ResourceInstance.server → Server** (多对一，可选)
- **ResourceInstance.cluster → Cluster** (多对一，可选)
- **ResourceInstance.project → Project** (多对一，可选)
- **ResourceInstance.idc → IDC** (多对一，可选)

## 🌐 页面路由

| URL | 功能 | 权限 |
|-----|------|------|
| /resource/idc/ | 机房列表 | menu_idc |
| /resource/server/ | 服务器列表 | menu_server |
| /resource/project/ | 项目列表 | menu_project |
| /resource/cluster/ | 集群列表 | menu_cluster |
| /resource/instance/ | 实例关联列表 | resource_instance_view |
| /resource/instance/add/ | 添加实例关联 | resource_instance_edit |
| /resource/instance/edit/<id>/ | 编辑实例关联 | resource_instance_edit |

## 🔐 权限系统

### 菜单权限

- `menu_resource` - 资源管理菜单
- `menu_idc` - 机房管理菜单
- `menu_server` - 服务器管理菜单
- `menu_project` - 项目管理菜单
- `menu_cluster` - 集群管理菜单

### 操作权限

#### 机房管理
- `idc_view` - 查看机房信息
- `idc_add` - 添加机房
- `idc_edit` - 编辑机房
- `idc_delete` - 删除机房

#### 服务器管理
- `server_view` - 查看服务器信息
- `server_add` - 添加服务器
- `server_edit` - 编辑服务器
- `server_delete` - 删除服务器

#### 项目管理
- `project_view` - 查看项目信息
- `project_add` - 添加项目
- `project_edit` - 编辑项目
- `project_delete` - 删除项目

#### 集群管理
- `cluster_view` - 查看集群信息
- `cluster_add` - 添加集群
- `cluster_edit` - 编辑集群
- `cluster_delete` - 删除集群

#### 实例关联
- `resource_instance_view` - 查看实例资源关联
- `resource_instance_edit` - 编辑实例资源关联

## 🚀 部署步骤

### 1. 数据库迁移

执行 SQL 迁移文件：

```bash
mysql -u用户名 -p数据库名 < src/init_sql/v2.0.0_resource_management.sql
```

### 2. Django 迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 配置权限

在 Django Admin 后台为用户或用户组分配相应的资源管理权限。

### 4. 启动服务

```bash
python manage.py runserver
```

## 📝 功能特性

### 1. 机房管理 (IDC)
- 机房基础信息管理（名称、编码、地址、联系人、电话、带宽）
- 机房状态管理（启用/停用）
- 关键字搜索（名称、编码、地址）
- 分页展示

### 2. 服务器管理 (Server)
- 服务器基础信息（名称、IP、内网IP、SSH配置）
- 硬件配置（CPU、内存、磁盘、操作系统）
- 服务器状态（在线/离线/维护）
- 所属机房关联
- 资源组权限隔离
- 多条件搜索和筛选

### 3. 项目管理 (Project)
- 项目基础信息（名称、编码、负责人）
- 项目优先级（高/中/低）
- 项目状态管理
- 资源组权限隔离

### 4. 集群管理 (Cluster)
- 集群基础信息（名称、编码）
- 集群类型（MySQL/Redis/MongoDB/PostgreSQL/Oracle/其他）
- 集群环境（生产/测试/开发）
- 所属项目关联
- 包含服务器管理

### 5. 实例资源关联 (ResourceInstance)
- 将现有数据库实例与资源模块关联
- 支持关联机房、服务器、项目、集群
- 环境类型标记
- 重要级别设置
- 备注信息

## 🎨 界面特性

- 统一的 Bootstrap 风格界面
- 搜索栏支持
- 数据筛选功能
- 分页展示
- 状态标签显示
- 权限控制的菜单展示

## 📊 数据库表结构

### resource_idc (机房表)
- idc_id - 机房ID
- idc_name - 机房名称
- idc_code - 机房编码
- idc_address - 机房地址
- idc_contact - 联系人
- idc_phone - 联系电话
- idc_bandwidth - 带宽信息
- idc_status - 状态
- idc_remark - 备注
- create_time - 创建时间
- update_time - 更新时间

### resource_server (服务器表)
- server_id - 服务器ID
- server_name - 服务器名称
- server_ip - 服务器IP
- server_inner_ip - 内网IP
- server_port - SSH端口
- server_username - SSH用户名
- server_password - SSH密码（加密）
- idc_id - 所属机房ID
- server_cpu - CPU信息
- server_memory - 内存信息
- server_disk - 磁盘信息
- server_os - 操作系统
- server_status - 状态
- server_role - 角色
- server_remark - 备注
- create_time - 创建时间
- update_time - 更新时间

### resource_project (项目表)
- project_id - 项目ID
- project_name - 项目名称
- project_code - 项目编码
- project_owner - 项目负责人
- project_owner_display - 负责人中文名
- project_description - 项目描述
- project_priority - 优先级
- project_status - 状态
- project_remark - 备注
- create_time - 创建时间
- update_time - 更新时间

### resource_cluster (集群表)
- cluster_id - 集群ID
- cluster_name - 集群名称
- cluster_code - 集群编码
- project_id - 所属项目ID
- cluster_type - 集群类型
- cluster_role - 集群角色
- cluster_status - 状态
- cluster_remark - 备注
- create_time - 创建时间
- update_time - 更新时间

### resource_instance (实例资源关联表)
- resource_instance_id - 关联ID
- instance_id - 数据库实例ID
- server_id - 所属服务器ID
- cluster_id - 所属集群ID
- project_id - 所属项目ID
- idc_id - 所属机房ID
- instance_env - 环境类型
- instance_level - 重要级别
- instance_remark - 备注
- create_time - 创建时间
- update_time - 更新时间

## 🤝 关联表

### resource_server_resource_group
- 服务器与资源组多对多关联

### resource_project_resource_group
- 项目与资源组多对多关联

### resource_cluster_servers
- 集群与服务器多对多关联

## 🔧 技术实现

- Django 4.0+
- Python 3.8+
- 数据加密（django-mirage-field）
- Bootstrap 前端框架
- jQuery 交互

## 📖 使用指南

### 快速开始

1. 先在后台创建机房信息
2. 添加服务器并关联到相应机房
3. 创建项目信息
4. 创建集群并关联项目和服务器
5. 将现有数据库实例通过ResourceInstance关联到资源

### 权限配置

在 `common/templates/base.html 中已集成资源管理菜单，根据用户权限自动显示。

## 📞 支持

如有问题，请参考项目原有文档或联系技术支持。
