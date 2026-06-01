# 资源管理模块 (Resource Management Module)

一个独立、可复用且支持可插拔机制的 Django 模块，用于管理数据库资源信息。

## 功能特性

- **机房信息管理** - 管理IDC机房信息
- **服务器信息管理** - 管理服务器信息，支持SSH密码加密存储
- **项目信息管理** - 管理项目信息，支持优先级配置
- **集群信息管理** - 管理数据库集群，支持多种数据库类型
- **实例资源关联** - 将数据库实例与资源管理模块关联
- **RESTful API** - 提供完整的API接口

## 模块特性

- 松耦合设计，易于集成和移除
- 支持配置化注册
- 提供清晰的API接口
- 完整的权限控制
- 支持配置启用/禁用子模块

## 安装与集成

### 1. 安装模块

将 `resource_management` 目录复制到 Django 项目目录中。

### 2. 配置 settings.py

```python
# settings.py

INSTALLED_APPS = [
    ...
    'resource_management',
    ...
]

# 可选配置
RESOURCE_MANAGEMENT = {
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
```

### 3. 配置 URLs

```python
# urls.py

from django.urls import path, include

urlpatterns = [
    ...
    path('resource/', include('resource_management.urls')),
    ...
]
```

### 4. 执行数据库迁移

```bash
python manage.py migrate resource_management
```

## URL 路由

| URL 路径 | 视图名称 | 功能描述 |
|---------|---------|---------|
| `/resource/idc/` | `idc_list` | 机房列表 |
| `/resource/server/` | `server_list` | 服务器列表 |
| `/resource/project/` | `project_list` | 项目列表 |
| `/resource/cluster/` | `cluster_list` | 集群列表 |
| `/resource/instance/` | `resource_instance_list` | 实例资源关联列表 |
| `/resource/instance/edit/<id>/` | `resource_instance_edit` | 编辑实例资源关联 |
| `/resource/instance/add/` | `resource_instance_add` | 添加实例资源关联 |
| `/resource/instance/delete/<id>/` | `resource_instance_delete` | 删除实例资源关联 |

## API 接口

### 机房列表 API

**GET** `/resource/api/idc/`

参数：
- `keyword` - 搜索关键词（可选）

返回示例：
```json
{
    "status": 0,
    "data": [
        {"id": 1, "name": "机房A", "code": "IDC-A-001"}
    ]
}
```

### 服务器列表 API

**GET** `/resource/api/server/`

参数：
- `idc_id` - 机房ID（可选）

返回示例：
```json
{
    "status": 0,
    "data": [
        {"id": 1, "name": "server-01", "ip": "192.168.1.100"}
    ]
}
```

### 项目列表 API

**GET** `/resource/api/project/`

参数：
- `keyword` - 搜索关键词（可选）

返回示例：
```json
{
    "status": 0,
    "data": [
        {"id": 1, "name": "项目A", "code": "PROJ-A-001"}
    ]
}
```

### 集群列表 API

**GET** `/resource/api/cluster/`

参数：
- `project_id` - 项目ID（可选）

返回示例：
```json
{
    "status": 0,
    "data": [
        {"id": 1, "name": "集群A", "type": "mysql"}
    ]
}
```

## 权限说明

模块提供以下权限：

| 权限代码 | 权限名称 | 说明 |
|---------|---------|------|
| `resource_management.view_idc` | 查看机房信息 | 查看机房列表 |
| `resource_management.add_idc` | 添加机房信息 | 添加新机房 |
| `resource_management.change_idc` | 修改机房信息 | 修改机房信息 |
| `resource_management.delete_idc` | 删除机房信息 | 删除机房 |
| `resource_management.view_server` | 查看服务器信息 | 查看服务器列表 |
| `resource_management.add_server` | 添加服务器信息 | 添加新服务器 |
| `resource_management.change_server` | 修改服务器信息 | 修改服务器信息 |
| `resource_management.delete_server` | 删除服务器信息 | 删除服务器 |
| `resource_management.view_project` | 查看项目信息 | 查看项目列表 |
| `resource_management.add_project` | 添加项目信息 | 添加新项目 |
| `resource_management.change_project` | 修改项目信息 | 修改项目信息 |
| `resource_management.delete_project` | 删除项目信息 | 删除项目 |
| `resource_management.view_cluster` | 查看集群信息 | 查看集群列表 |
| `resource_management.add_cluster` | 添加集群信息 | 添加新集群 |
| `resource_management.change_cluster` | 修改集群信息 | 修改集群信息 |
| `resource_management.delete_cluster` | 删除集群信息 | 删除集群 |
| `resource_management.view_resourceinstance` | 查看实例资源关联 | 查看关联列表 |
| `resource_management.add_resourceinstance` | 添加实例资源关联 | 添加新关联 |
| `resource_management.change_resourceinstance` | 修改实例资源关联 | 修改关联信息 |
| `resource_management.delete_resourceinstance` | 删除实例资源关联 | 删除关联 |

## 数据模型

### IDC（机房信息）

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `idc_id` | Integer | 主键 |
| `idc_name` | String | 机房名称（唯一） |
| `idc_code` | String | 机房编码（唯一） |
| `idc_address` | String | 机房地址 |
| `idc_contact` | String | 联系人 |
| `idc_phone` | String | 联系电话 |
| `idc_bandwidth` | String | 带宽信息 |
| `idc_status` | Integer | 状态（0=停用，1=启用） |
| `idc_remark` | Text | 备注 |
| `create_time` | DateTime | 创建时间 |
| `update_time` | DateTime | 更新时间 |

### Server（服务器信息）

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `server_id` | Integer | 主键 |
| `server_name` | String | 服务器名称（唯一） |
| `server_ip` | String | 服务器IP |
| `server_inner_ip` | String | 内网IP |
| `server_port` | Integer | SSH端口 |
| `server_username` | String | SSH用户名 |
| `server_password` | EncryptedChar | SSH密码（加密存储） |
| `idc` | ForeignKey | 所属机房 |
| `server_cpu` | String | CPU信息 |
| `server_memory` | String | 内存信息 |
| `server_disk` | String | 磁盘信息 |
| `server_os` | String | 操作系统 |
| `server_status` | Integer | 状态（0=离线，1=在线，2=维护） |
| `server_role` | String | 角色 |
| `server_remark` | Text | 备注 |
| `create_time` | DateTime | 创建时间 |
| `update_time` | DateTime | 更新时间 |

### Project（项目信息）

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `project_id` | Integer | 主键 |
| `project_name` | String | 项目名称（唯一） |
| `project_code` | String | 项目编码（唯一） |
| `project_owner` | String | 项目负责人 |
| `project_owner_display` | String | 负责人中文名 |
| `project_description` | Text | 项目描述 |
| `project_priority` | Integer | 优先级（1=高，2=中，3=低） |
| `project_status` | Integer | 状态（0=停用，1=启用） |
| `project_remark` | Text | 备注 |
| `create_time` | DateTime | 创建时间 |
| `update_time` | DateTime | 更新时间 |

### Cluster（集群信息）

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `cluster_id` | Integer | 主键 |
| `cluster_name` | String | 集群名称（唯一） |
| `cluster_code` | String | 集群编码（唯一） |
| `project` | ForeignKey | 所属项目 |
| `cluster_type` | String | 集群类型 |
| `cluster_role` | String | 集群角色 |
| `servers` | ManyToMany | 包含服务器 |
| `cluster_status` | Integer | 状态（0=停用，1=启用） |
| `cluster_remark` | Text | 备注 |
| `create_time` | DateTime | 创建时间 |
| `update_time` | DateTime | 更新时间 |

### ResourceInstance（实例资源关联）

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `resource_instance_id` | Integer | 主键 |
| `instance_id` | Integer | 数据库实例ID |
| `instance_name` | String | 实例名称 |
| `server` | ForeignKey | 所属服务器 |
| `cluster` | ForeignKey | 所属集群 |
| `project` | ForeignKey | 所属项目 |
| `idc` | ForeignKey | 所属机房 |
| `instance_env` | String | 环境类型 |
| `instance_level` | Integer | 重要级别 |
| `instance_remark` | Text | 备注 |
| `create_time` | DateTime | 创建时间 |
| `update_time` | DateTime | 更新时间 |

## 模型关系图

```
IDC (机房)
    |
    +---< Server (服务器)
              |
              +---< Cluster.servers (集群-服务器 多对多)
    |
    +---< ResourceInstance (实例资源关联)

Project (项目)
    |
    +---< Cluster (集群)
              |
              +---< ResourceInstance (实例资源关联)

Cluster (集群)
    |
    +---< ResourceInstance (实例资源关联)

Server (服务器)
    |
    +---< ResourceInstance (实例资源关联)
```

## 使用注册工具

模块提供了便捷的注册工具：

```python
import resource_management

# 注册模块
resource_management.register_resource_management()

# 获取URL配置
urlpatterns += resource_management.get_urls()

# 获取菜单项
menu_items = resource_management.get_menu_items()

# 检查是否已安装
is_installed = resource_management.is_installed()

# 卸载模块
resource_management.uninstall_resource_management()

# 获取权限列表
permissions = resource_management.get_permissions()
```

## 运行单元测试

```bash
python manage.py test resource_management.tests
```

## 卸载模块

### 1. 移除配置

从 `settings.py` 中移除 `resource_management`。

### 2. 移除 URL 配置

从 `urls.py` 中移除资源管理模块的 URL 配置。

### 3. 可选：删除数据库表

```sql
DROP TABLE resource_idc;
DROP TABLE resource_server;
DROP TABLE resource_project;
DROP TABLE resource_cluster;
DROP TABLE resource_cluster_servers;
DROP TABLE resource_instance;
```

## 版本信息

- **版本**: 1.0.0
- **依赖**: Django 3.0+
- **加密**: django-mirage-field

## 许可证

MIT License
