-- 资源管理模块数据库迁移
-- 创建机房信息表
CREATE TABLE IF NOT EXISTS `resource_idc` (
  `idc_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '机房ID',
  `idc_name` varchar(100) NOT NULL COMMENT '机房名称',
  `idc_code` varchar(50) NOT NULL COMMENT '机房编码',
  `idc_address` varchar(255) DEFAULT '' COMMENT '机房地址',
  `idc_contact` varchar(50) DEFAULT '' COMMENT '联系人',
  `idc_phone` varchar(20) DEFAULT '' COMMENT '联系电话',
  `idc_bandwidth` varchar(100) DEFAULT '' COMMENT '带宽信息',
  `idc_status` int(11) NOT NULL DEFAULT '1' COMMENT '状态 0-停用 1-启用',
  `idc_remark` text COMMENT '备注',
  `create_time` datetime(6) NOT NULL COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`idc_id`),
  UNIQUE KEY `resource_idc_idc_name_uniq` (`idc_name`),
  UNIQUE KEY `resource_idc_idc_code_uniq` (`idc_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='机房信息';

-- 创建服务器信息表
CREATE TABLE IF NOT EXISTS `resource_server` (
  `server_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '服务器ID',
  `server_name` varchar(100) NOT NULL COMMENT '服务器名称',
  `server_ip` varchar(100) NOT NULL COMMENT '服务器IP',
  `server_inner_ip` varchar(100) DEFAULT '' COMMENT '内网IP',
  `server_port` int(11) NOT NULL DEFAULT '22' COMMENT 'SSH端口',
  `server_username` varchar(50) NOT NULL DEFAULT 'root' COMMENT 'SSH用户名',
  `server_password` varchar(255) DEFAULT '' COMMENT 'SSH密码',
  `idc_id` int(11) DEFAULT NULL COMMENT '所属机房ID',
  `server_cpu` varchar(255) DEFAULT '' COMMENT 'CPU信息',
  `server_memory` varchar(255) DEFAULT '' COMMENT '内存信息',
  `server_disk` varchar(255) DEFAULT '' COMMENT '磁盘信息',
  `server_os` varchar(100) DEFAULT '' COMMENT '操作系统',
  `server_status` int(11) NOT NULL DEFAULT '1' COMMENT '状态 0-离线 1-在线 2-维护',
  `server_role` varchar(50) DEFAULT '' COMMENT '角色',
  `server_remark` text COMMENT '备注',
  `create_time` datetime(6) NOT NULL COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`server_id`),
  UNIQUE KEY `resource_server_server_name_uniq` (`server_name`),
  KEY `resource_server_idc_id_fk_resource_idc_idc_id` (`idc_id`),
  CONSTRAINT `resource_server_idc_id_fk_resource_idc_idc_id` FOREIGN KEY (`idc_id`) REFERENCES `resource_idc` (`idc_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='服务器信息';

-- 创建服务器与资源组关联表
CREATE TABLE IF NOT EXISTS `resource_server_resource_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_id` int(11) NOT NULL,
  `resourcegroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `resource_server_resource_group_server_id_resourcegroup_id_uniq` (`server_id`,`resourcegroup_id`),
  KEY `resource_server_resource_group_resourcegroup_id_fk_resource_group_group_id` (`resourcegroup_id`),
  CONSTRAINT `resource_server_resource_group_resourcegroup_id_fk_resource_group_group_id` FOREIGN KEY (`resourcegroup_id`) REFERENCES `resource_group` (`group_id`) ON DELETE CASCADE,
  CONSTRAINT `resource_server_resource_group_server_id_fk_resource_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `resource_server` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建项目信息表
CREATE TABLE IF NOT EXISTS `resource_project` (
  `project_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '项目ID',
  `project_name` varchar(100) NOT NULL COMMENT '项目名称',
  `project_code` varchar(50) NOT NULL COMMENT '项目编码',
  `project_owner` varchar(50) DEFAULT '' COMMENT '项目负责人',
  `project_owner_display` varchar(50) DEFAULT '' COMMENT '负责人中文名',
  `project_description` text COMMENT '项目描述',
  `project_priority` int(11) NOT NULL DEFAULT '2' COMMENT '优先级 1-高 2-中 3-低',
  `project_status` int(11) NOT NULL DEFAULT '1' COMMENT '状态 0-停用 1-启用',
  `project_remark` text COMMENT '备注',
  `create_time` datetime(6) NOT NULL COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`project_id`),
  UNIQUE KEY `resource_project_project_name_uniq` (`project_name`),
  UNIQUE KEY `resource_project_project_code_uniq` (`project_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目信息';

-- 创建项目与资源组关联表
CREATE TABLE IF NOT EXISTS `resource_project_resource_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `resourcegroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `resource_project_resource_group_project_id_resourcegroup_id_uniq` (`project_id`,`resourcegroup_id`),
  KEY `resource_project_resource_group_resourcegroup_id_fk_resource_group_group_id` (`resourcegroup_id`),
  CONSTRAINT `resource_project_resource_group_resourcegroup_id_fk_resource_group_group_id` FOREIGN KEY (`resourcegroup_id`) REFERENCES `resource_group` (`group_id`) ON DELETE CASCADE,
  CONSTRAINT `resource_project_resource_group_project_id_fk_resource_project_project_id` FOREIGN KEY (`project_id`) REFERENCES `resource_project` (`project_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建集群信息表
CREATE TABLE IF NOT EXISTS `resource_cluster` (
  `cluster_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '集群ID',
  `cluster_name` varchar(100) NOT NULL COMMENT '集群名称',
  `cluster_code` varchar(50) NOT NULL COMMENT '集群编码',
  `project_id` int(11) DEFAULT NULL COMMENT '所属项目ID',
  `cluster_type` varchar(50) NOT NULL COMMENT '集群类型',
  `cluster_role` varchar(50) NOT NULL DEFAULT 'production' COMMENT '集群角色 production-生产 test-测试 dev-开发',
  `cluster_status` int(11) NOT NULL DEFAULT '1' COMMENT '状态 0-停用 1-启用',
  `cluster_remark` text COMMENT '备注',
  `create_time` datetime(6) NOT NULL COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`cluster_id`),
  UNIQUE KEY `resource_cluster_cluster_name_uniq` (`cluster_name`),
  UNIQUE KEY `resource_cluster_cluster_code_uniq` (`cluster_code`),
  KEY `resource_cluster_project_id_fk_resource_project_project_id` (`project_id`),
  CONSTRAINT `resource_cluster_project_id_fk_resource_project_project_id` FOREIGN KEY (`project_id`) REFERENCES `resource_project` (`project_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='集群信息';

-- 创建集群与服务器关联表
CREATE TABLE IF NOT EXISTS `resource_cluster_servers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cluster_id` int(11) NOT NULL,
  `server_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `resource_cluster_servers_cluster_id_server_id_uniq` (`cluster_id`,`server_id`),
  KEY `resource_cluster_servers_server_id_fk_resource_server_server_id` (`server_id`),
  CONSTRAINT `resource_cluster_servers_cluster_id_fk_resource_cluster_cluster_id` FOREIGN KEY (`cluster_id`) REFERENCES `resource_cluster` (`cluster_id`) ON DELETE CASCADE,
  CONSTRAINT `resource_cluster_servers_server_id_fk_resource_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `resource_server` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建实例资源关联表
CREATE TABLE IF NOT EXISTS `resource_instance` (
  `resource_instance_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '关联ID',
  `instance_id` int(11) NOT NULL COMMENT '数据库实例ID',
  `server_id` int(11) DEFAULT NULL COMMENT '所属服务器ID',
  `cluster_id` int(11) DEFAULT NULL COMMENT '所属集群ID',
  `project_id` int(11) DEFAULT NULL COMMENT '所属项目ID',
  `idc_id` int(11) DEFAULT NULL COMMENT '所属机房ID',
  `instance_env` varchar(20) NOT NULL DEFAULT 'prod' COMMENT '环境类型 prod-生产 test-测试 dev-开发',
  `instance_level` int(11) NOT NULL DEFAULT '2' COMMENT '重要级别 1-核心 2-重要 3-一般',
  `instance_remark` text COMMENT '备注',
  `create_time` datetime(6) NOT NULL COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`resource_instance_id`),
  UNIQUE KEY `resource_instance_instance_id_uniq` (`instance_id`),
  KEY `resource_instance_cluster_id_fk_resource_cluster_cluster_id` (`cluster_id`),
  KEY `resource_instance_idc_id_fk_resource_idc_idc_id` (`idc_id`),
  KEY `resource_instance_project_id_fk_resource_project_project_id` (`project_id`),
  KEY `resource_instance_server_id_fk_resource_server_server_id` (`server_id`),
  CONSTRAINT `resource_instance_cluster_id_fk_resource_cluster_cluster_id` FOREIGN KEY (`cluster_id`) REFERENCES `resource_cluster` (`cluster_id`) ON DELETE CASCADE,
  CONSTRAINT `resource_instance_idc_id_fk_resource_idc_idc_id` FOREIGN KEY (`idc_id`) REFERENCES `resource_idc` (`idc_id`) ON DELETE CASCADE,
  CONSTRAINT `resource_instance_instance_id_fk_sql_instance_id` FOREIGN KEY (`instance_id`) REFERENCES `sql_instance` (`id`) ON DELETE CASCADE,
  CONSTRAINT `resource_instance_project_id_fk_resource_project_project_id` FOREIGN KEY (`project_id`) REFERENCES `resource_project` (`project_id`) ON DELETE CASCADE,
  CONSTRAINT `resource_instance_server_id_fk_resource_server_server_id` FOREIGN KEY (`server_id`) REFERENCES `resource_server` (`server_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='实例资源关联';

-- 添加资源管理模块的权限
-- 菜单权限
INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '菜单 资源管理', id, 'menu_resource'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '菜单 机房管理', id, 'menu_idc'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '菜单 服务器管理', id, 'menu_server'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '菜单 项目管理', id, 'menu_project'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '菜单 集群管理', id, 'menu_cluster'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

-- 机房管理权限
INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '查看机房信息', id, 'idc_view'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '添加机房', id, 'idc_add'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '编辑机房', id, 'idc_edit'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '删除机房', id, 'idc_delete'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

-- 服务器管理权限
INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '查看服务器信息', id, 'server_view'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '添加服务器', id, 'server_add'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '编辑服务器', id, 'server_edit'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '删除服务器', id, 'server_delete'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

-- 项目管理权限
INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '查看项目信息', id, 'project_view'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '添加项目', id, 'project_add'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '编辑项目', id, 'project_edit'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '删除项目', id, 'project_delete'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

-- 集群管理权限
INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '查看集群信息', id, 'cluster_view'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '添加集群', id, 'cluster_add'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '编辑集群', id, 'cluster_edit'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '删除集群', id, 'cluster_delete'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

-- 实例关联权限
INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '查看实例资源关联', id, 'resource_instance_view'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

INSERT INTO `auth_permission` (`name`, `content_type_id`, `codename`)
SELECT '编辑实例资源关联', id, 'resource_instance_edit'
FROM `django_content_type`
WHERE `app_label` = 'sql' AND `model` = 'permission'
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);
