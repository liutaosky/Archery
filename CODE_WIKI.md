# Archery Code Wiki

## 目录
1. [项目概述](#项目概述)
2. [系统架构](#系统架构)
3. [核心模块详解](#核心模块详解)
4. [数据库设计](#数据库设计)
5. [API接口设计](#api接口设计)
6. [依赖关系](#依赖关系)
7. [部署与配置](#部署与配置)

---

## 项目概述

### 项目简介
Archery 是一个企业级的 SQL 审核查询平台，旨在提升 DBA 的工作效率，支持多种数据库的 SQL 上线和查询，同时提供丰富的数据库运维功能。该项目源于 archer 的分支，现已发展成为一个功能完善的数据库管理系统。

### 核心功能
- **查询功能**：支持多种数据库类型的在线查询
- **SQL审核**：自动化的 SQL 语法检查和审核流程
- **执行管理**：SQL 工单的审核、执行和回滚
- **数据备份**：支持执行前的数据备份
- **数据字典**：数据库结构文档的生成和导出
- **慢日志分析**：慢查询日志的统计和优化建议
- **会话管理**：数据库会话查看和终止
- **账号管理**：实例账号的创建、修改和权限管理
- **参数管理**：实例参数的查看和修改
- **数据归档**：历史数据的归档和清理

### 支持的数据库类型
| 数据库类型 | 查询 | 审核 | 执行 | 备份 | 数据字典 | 慢日志 |
|-----------|------|------|------|------|---------|--------|
| MySQL     | √    | √    | √    | √    | √       | √      |
| MsSQL     | √    | ×    | √    | ×    | √       | ×      |
| Redis     | √    | ×    | √    | ×    | ×       | ×      |
| PgSQL     | √    | ×    | √    | ×    | ×       | ×      |
| Oracle    | √    | √    | √    | √    | √       | ×      |
| MongoDB   | √    | √    | √    | ×    | ×       | ×      |
| Phoenix   | √    | ×    | √    | ×    | ×       | ×      |
| ODPS      | √    | ×    | ×    | ×    | ×       | ×      |
| ClickHouse| √    | √    | √    | ×    | ×       | ×      |

---

## 系统架构

### 技术栈

#### 后端框架
- **Web框架**：Django 4.0.5
- **任务队列**：django-q
- **API框架**：Django REST Framework

#### 前端技术
- **UI框架**：Bootstrap
- **JavaScript库**：jQuery
- **图表库**：ECharts (通过 pyecharts)
- **代码编辑器**：Ace Editor

#### 数据库驱动
- MySQL：mysqlclient
- MsSQL：pyodbc
- Redis：redis-py
- PostgreSQL：psycopg2
- Oracle：cx_Oracle
- MongoDB：pymongo
- Phoenix：phoenixdb
- ODPS：pyodps
- ClickHouse：clickhouse-driver

#### 功能依赖
- SQL审核：goInception / inception
- SQL优化：SQLAdvisor / SOAR
- Binlog解析：python-mysql-replication
- 表结构同步：SchemaSync
- 云服务集成：阿里云 SDK

### 目录结构

```
/workspace/
├── archery/              # Django项目配置
│   ├── __init__.py
│   ├── settings.py       # 项目配置文件
│   ├── urls.py           # 主URL路由
│   ├── asgi.py
│   └── wsgi.py
├── common/               # 公共模块
│   ├── middleware/       # 中间件
│   │   ├── check_login_middleware.py
│   │   └── exception_logging_middleware.py
│   ├── static/           # 静态资源
│   ├── templates/        # 公共模板
│   ├── twofa/            # 双因素认证
│   ├── utils/            # 工具函数
│   ├── auth.py           # 认证相关
│   ├── check.py          # 检查工具
│   ├── config.py         # 配置管理
│   ├── dashboard.py      # 仪表盘
│   ├── storage.py        # 存储管理
│   ├── views.py          # 公共视图
│   └── workflow.py       # 工作流
├── sql/                  # SQL管理核心模块
│   ├── engines/          # 数据库引擎
│   │   ├── mysql.py      # MySQL引擎
│   │   ├── mssql.py      # MsSQL引擎
│   │   ├── pgsql.py      # PostgreSQL引擎
│   │   ├── oracle.py     # Oracle引擎
│   │   ├── mongo.py      # MongoDB引擎
│   │   ├── redis.py      # Redis引擎
│   │   ├── clickhouse.py # ClickHouse引擎
│   │   ├── odps.py       # ODPS引擎
│   │   ├── phoenix.py    # Phoenix引擎
│   │   └── goinception.py# goInception引擎
│   ├── plugins/          # 插件模块
│   ├── utils/            # SQL工具函数
│   ├── templates/        # SQL相关模板
│   ├── models.py         # 数据模型
│   ├── sql_workflow.py   # SQL工作流
│   ├── query.py          # 查询功能
│   ├── instance.py       # 实例管理
│   ├── slowlog.py        # 慢日志
│   └── ...
├── sql_api/              # RESTful API模块
│   ├── api_instance.py
│   ├── api_user.py
│   ├── api_workflow.py
│   ├── serializers.py
│   ├── permissions.py
│   └── urls.py
├── src/                  # 源代码和配置
│   ├── charts/           # 图表相关
│   ├── docker/           # Docker配置
│   ├── docker-compose/   # docker-compose配置
│   ├── init_sql/         # 初始化SQL
│   └── plugins/          # 插件配置
├── downloads/            # 下载目录
├── logs/                 # 日志目录
├── manage.py             # Django管理脚本
└── requirements.txt      # Python依赖
```

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         前端层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   仪表盘     │  │  SQL管理界面  │  │   系统管理界面   │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       应用层(Django)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   sql模块    │  │  sql_api模块 │  │   common模块     │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                         业务逻辑层                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │SQL审核   │ │工作流管理 │ │查询管理   │ │实例管理   │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       数据库引擎层                            │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐          │
│  │MySQL │ │Oracle│ │MsSQL │ │PgSQL │ │其他引擎  │          │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      外部服务层                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │goInception│ │SQLAdvisor│ │  SOAR    │ │云服务API  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心模块详解

### 1. archery 模块 - 项目配置

#### settings.py 核心配置
```python
# 数据库配置
DATABASES = {
    'default': {
        ...
    }
}

# Django Q任务队列配置
Q_CLUSTER = {
    'name': 'archery',
    'workers': 4,
    'timeout': 60,
    ...
}

# REST Framework配置
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [...],
    ...
}

# 自定义用户模型
AUTH_USER_MODEL = "sql.Users"
```

#### urls.py 主路由
- `/admin/` - Django管理后台
- `/api/` - RESTful API接口
- `/` - 主应用路由（包含所有业务功能）

### 2. common 模块 - 公共功能

#### 中间件 (middleware/)
- **check_login_middleware.py**：登录验证中间件，检查用户是否已登录
- **exception_logging_middleware.py**：异常日志记录中间件

#### 工具函数 (utils/)
- **permission.py**：权限检查工具
- **sendmsg.py**：消息发送工具（钉钉、飞书、企业微信等）
- **ding_api.py**：钉钉API集成
- **feishu_api.py**：飞书API集成
- **aliyun_sms.py**：阿里云短信服务
- **global_info.py**：全局信息管理
- **convert.py**：数据转换工具
- **timer.py**：定时器工具
- **aes_decryptor.py**：AES加解密

#### 双因素认证 (twofa/)
- **totp.py**：TOTP（基于时间的一次性密码）实现
- **sms.py**：短信验证码实现

### 3. sql 模块 - SQL管理核心

#### 3.1 数据模型 (models.py)

**核心模型类：**

| 模型类 | 说明 | 主要字段 |
|--------|------|----------|
| `Users` | 用户信息（扩展Django User） | username, display, ding_user_id, failed_login_count |
| `ResourceGroup` | 资源组 | group_name, group_parent_id, ding_webhook |
| `Instance` | 数据库实例配置 | instance_name, db_type, host, port, user, password |
| `InstanceTag` | 实例标签 | tag_code, tag_name |
| `Tunnel` | SSH隧道配置 | tunnel_name, host, port, user, password |
| `SqlWorkflow` | SQL工单 | workflow_name, instance, db_name, status, engineer |
| `SqlWorkflowContent` | SQL工单内容 | sql_content, review_content, execute_result |
| `WorkflowAudit` | 工作流审核 | audit_id, workflow_id, current_status |
| `WorkflowAuditDetail` | 审核明细 | audit_id, audit_user, audit_status |
| `QueryPrivilegesApply` | 查询权限申请 | apply_id, user_name, instance, valid_date |
| `QueryPrivileges` | 查询权限记录 | privilege_id, user_name, instance, db_name |
| `QueryLog` | 查询日志 | instance_name, db_name, sqllog, username |
| `DataMaskingColumns` | 脱敏字段配置 | rule_type, instance, table_name, column_name |
| `DataMaskingRules` | 脱敏规则配置 | rule_type, rule_regex, hide_group |
| `InstanceAccount` | 实例账号 | instance, user, host, password |
| `InstanceDatabase` | 实例数据库 | instance, db_name, owner |
| `ArchiveConfig` | 归档配置 | title, src_instance, src_db_name, condition |
| `ArchiveLog` | 归档日志 | archive, select_cnt, insert_cnt, delete_cnt |
| `ParamTemplate` | 参数模板 | db_type, variable_name, default_value |
| `ParamHistory` | 参数修改历史 | instance, variable_name, old_var, new_var |
| `SlowQuery` | 慢查询统计 | checksum, fingerprint, sample |
| `SlowQueryHistory` | 慢查询历史 | checksum, ts_min, ts_max, query_time_sum |
| `AuditEntry` | 审计日志 | user_id, action, action_time |
| `Config` | 系统配置 | item, value, description |
| `CloudAccessKey` | 云服务认证 | type, key_id, key_secret |
| `AliyunRdsConfig` | 阿里云RDS配置 | instance, rds_dbinstanceid, ak |

#### 3.2 SQL工作流 (sql_workflow.py)

**主要功能：**
- SQL工单提交与自动审核
- 工单审核流程管理
- SQL执行与结果记录
- 数据备份
- 定时任务执行
- OSC（Online Schema Change）控制

**关键函数：**
- `submit()` - 提交SQL工单
- `passed()` - 审核通过
- `execute()` - 执行SQL
- `timing_task()` - 定时任务
- `cancel()` - 取消工单
- `get_workflow_status()` - 获取工单状态

**工单状态流转：**
```
提交 → 人工审核中 → 审核通过 → 排队中 → 执行中 → 执行完成
                    ↓
                  审核拒绝
```

#### 3.3 查询功能 (query.py)

**主要功能：**
- 在线SQL查询
- 查询权限验证
- 数据脱敏
- 查询日志记录
- 收藏查询语句

**关键函数：**
- `query()` - 执行SQL查询
- `querylog()` - 查询日志列表
- `favorite()` - 收藏管理
- `explain()` - SQL执行计划

#### 3.4 实例管理 (instance.py)

**主要功能：**
- 实例列表管理
- 实例资源管理
- 表结构同步
- 表结构描述
- 参数管理

**关键函数：**
- `lists()` - 实例列表
- `instance_resource()` - 实例资源
- `describe()` - 表结构描述
- `schemasync()` - 表结构同步
- `param_list()` - 参数列表
- `param_edit()` - 参数编辑

#### 3.5 慢日志管理 (slowlog.py)

**主要功能：**
- 慢查询日志查看
- 慢查询统计分析
- 慢查询优化建议

**关键函数：**
- `slowquery_review()` - 慢查询统计
- `slowquery_review_history()` - 慢查询历史
- `report()` - 生成报告

#### 3.6 数据字典 (data_dictionary.py)

**主要功能：**
- 表结构展示
- 字段信息查看
- 数据字典导出

**关键函数：**
- `table_list()` - 表列表
- `table_info()` - 表信息
- `export()` - 导出数据字典

#### 3.7 数据归档 (archiver.py)

**主要功能：**
- 归档配置管理
- 归档申请与审核
- 归档执行
- 归档日志

**关键函数：**
- `archive_list()` - 归档列表
- `archive_apply()` - 归档申请
- `archive_audit()` - 归档审核
- `archive_once()` - 立即归档
- `archive_log()` - 归档日志

#### 3.8 数据库引擎 (engines/)

**引擎基类设计：**
每种数据库类型都有对应的引擎实现，提供统一的接口。

**MySQL引擎 (mysql.py)：**
- 连接管理
- 查询执行
- 元数据获取
- 备份恢复
- Binlog解析

**goInception引擎 (goinception.py)：**
- SQL审核
- SQL执行
- 备份功能

**其他引擎：**
- `mssql.py` - SQL Server
- `pgsql.py` - PostgreSQL
- `oracle.py` - Oracle
- `mongo.py` - MongoDB
- `redis.py` - Redis
- `clickhouse.py` - ClickHouse
- `phoenix.py` - Phoenix
- `odps.py` - ODPS

#### 3.9 工具函数 (utils/)

| 模块 | 功能 |
|------|------|
| `execute_sql.py` | SQL执行工具 |
| `sql_review.py` | SQL审核规则 |
| `sql_utils.py` | SQL工具函数 |
| `data_masking.py` | 数据脱敏 |
| `extract_tables.py` | 提取SQL中的表名 |
| `resource_group.py` | 资源组工具 |
| `workflow_audit.py` | 工作流审核 |
| `ssh_tunnel.py` | SSH隧道 |
| `tasks.py` | 异步任务 |

### 4. sql_api 模块 - RESTful API

#### 主要接口文件
- `api_instance.py` - 实例相关API
- `api_user.py` - 用户相关API
- `api_workflow.py` - 工作流相关API
- `serializers.py` - 序列化器
- `permissions.py` - 权限控制
- `pagination.py` - 分页

#### 认证方式
- JWT (JSON Web Token)
- Session认证

#### API文档
使用 drf-spectacular 生成 OpenAPI 3.0 文档

---

## 数据库设计

### 核心表关系图

```
Users ──┬──> QueryPrivileges
        │
        ├──> QueryLog
        │
        ├──> AuditEntry
        │
        └──> [ManyToMany] ResourceGroup

ResourceGroup ──┬──> [ManyToMany] Instance
                │
                ├──> ArchiveConfig
                │
                └──> WorkflowAuditSetting

Instance ──┬──> SqlWorkflow
           │
           ├──> InstanceAccount
           │
           ├──> InstanceDatabase
           │
           ├──> DataMaskingColumns
           │
           ├──> ArchiveConfig (src_instance)
           │
           ├──> ArchiveConfig (dest_instance)
           │
           ├──> ParamHistory
           │
           ├──> QueryPrivilegesApply
           │
           ├──> QueryPrivileges
           │
           └──> AliyunRdsConfig

SqlWorkflow ──┬──> SqlWorkflowContent (OneToOne)
              │
              └──> WorkflowAudit

WorkflowAudit ──> WorkflowAuditDetail

ArchiveConfig ──> ArchiveLog

SlowQuery ──> SlowQueryHistory
```

### 关键表说明

#### sql_users (Users模型)
存储用户信息，扩展自Django的AbstractUser。
- 支持钉钉、企业微信、飞书用户ID
- 登录失败次数统计
- 资源组关联

#### sql_instance (Instance模型)
存储数据库实例配置信息。
- 支持多种数据库类型
- 支持主从配置
- 支持SSH隧道连接
- 敏感信息加密存储

#### sql_workflow (SqlWorkflow模型)
存储SQL工单基本信息。
- 工单状态管理
- 关联实例和数据库
- 审核流程记录

#### sql_workflow_content (SqlWorkflowContent模型)
存储SQL工单的详细内容。
- SQL内容
- 审核结果
- 执行结果

#### query_privileges (QueryPrivileges模型)
管理用户查询权限。
- 数据库级权限
- 表级权限
- 有效期管理
- 行数限制

#### data_masking_columns (DataMaskingColumns模型)
配置需要脱敏的字段。
- 关联脱敏规则
- 按实例、库、表、字段配置

---

## API接口设计

### 认证接口

### 实例管理API

### 工作流API

### 查询API

---

## 依赖关系

### Python依赖 (requirements.txt)

```
Django==4.0.5
mysqlclient==2.0.3
requests==2.28.0
simplejson==3.17.2
mybatis_mapper2sql==0.1.9
django-auth-ldap==4.1.0
python-dateutil==2.8.1
pymongo==3.11.0
psycopg2-binary==2.8.6
pymysql==0.9.3
mysql-replication==0.22
django-q==1.3.9
django-redis==5.2.0
pyodbc==4.0.30
gunicorn==20.0.4
pyecharts==1.9.1
aliyun-python-sdk-rds==2.1.1
cx-Oracle==7.3.0
supervisor==4.1.0
phoenixdb==0.7
django-mirage-field==1.4.0
schema-sync==0.9.7
parsedatetime==2.4
sshtunnel==0.1.5
pycryptodome==3.10.1
pandas==1.1.5
pyodps==0.10.7.1
clickhouse-driver==0.2.3
djangorestframework==3.13.1
djangorestframework-simplejwt==5.2.0
django-filter==21.1
drf-spectacular==0.22.0
pyotp==2.6.0
pillow==9.0.1
qrcode==7.3.1
django-environ
alibabacloud_dysmsapi20170525==2.0.9
tencentcloud-sdk-python==3.0.656
```

### 外部工具依赖

| 工具 | 用途 |
|------|------|
| goInception | SQL审核和执行 |
| SQLAdvisor | SQL优化建议 |
| SOAR | SQL优化和分析 |
| SchemaSync | 表结构同步 |
| pt-query-digest | 慢日志分析 |
| my2sql | Binlog解析 |
| gh-ost | 在线DDL |
| pt-online-schema-change | 在线DDL |

---

## 部署与配置

### Docker部署

1. 准备docker-compose配置
2. 启动服务
3. 初始化数据库
4. 创建管理员用户
5. 访问系统

### 手动部署

1. 安装Python依赖
2. 配置数据库
3. 配置Redis
4. 初始化Django
5. 配置Nginx
6. 启动服务

### 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| SECRET_KEY | Django密钥 | 自动生成 |
| DEBUG | 调试模式 | False |
| DATABASE_URL | 数据库连接 | mysql://root:@127.0.0.1:3306/archery |
| CACHE_URL | Redis缓存连接 | redis://127.0.0.1:6379/0 |
| ENABLE_LDAP | 启用LDAP认证 | False |

### 系统配置项

系统配置存储在 `sql_config` 表中，包含：
- 邮件服务配置
- 钉钉机器人配置
- 飞书机器人配置
- 企业微信机器人配置
- goInception配置
- SOAR配置
- 其他功能开关

---

## 开发指南

### 代码规范
- 遵循PEP 8 Python编码规范
- 使用Django最佳实践
- 保持代码注释和文档更新

### 扩展新数据库引擎

1. 在 `sql/engines/` 目录下创建新的引擎文件
2. 实现统一的接口方法
3. 在 `DB_TYPE_CHOICES` 中添加新类型
4. 更新相关的视图和模板

### 添加新的审核规则

1. 在 `sql/utils/sql_review.py` 中添加规则
2. 更新前端展示
3. 编写测试用例

---

## 常见问题

### 1. 如何添加新的数据库类型支持？
详见「扩展新数据库引擎」章节。

### 2. 如何配置LDAP认证？
在 `settings.py` 中配置 `ENABLE_LDAP=True` 及相关LDAP参数。

### 3. 如何开启双因素认证？
用户可在个人设置中开启TOTP或短信认证。

---

*本Wiki文档最后更新：2026-05-28*
