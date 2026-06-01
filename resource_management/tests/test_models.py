# -*- coding: UTF-8 -*-
"""
资源管理模块模型单元测试
"""
import unittest
from django.test import TestCase
from django.core.exceptions import ValidationError

from resource_management.models import IDC, Server, Project, Cluster, ResourceInstance


class IDCTestCase(TestCase):
    """
    机房信息模型测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.idc = IDC.objects.create(
            idc_name='测试机房',
            idc_code='TEST-IDC-001',
            idc_address='北京市海淀区',
            idc_contact='张三',
            idc_phone='13800138000',
            idc_bandwidth='100M',
            idc_status=1,
            idc_remark='测试机房'
        )
    
    def test_idc_creation(self):
        """
        测试机房创建
        """
        self.assertEqual(self.idc.idc_name, '测试机房')
        self.assertEqual(self.idc.idc_code, 'TEST-IDC-001')
        self.assertEqual(self.idc.idc_status, 1)
    
    def test_idc_str(self):
        """
        测试机房字符串表示
        """
        self.assertEqual(str(self.idc), '测试机房')
    
    def test_idc_unique_constraint(self):
        """
        测试机房唯一约束
        """
        with self.assertRaises(Exception):
            IDC.objects.create(
                idc_name='测试机房',
                idc_code='TEST-IDC-002'
            )


class ServerTestCase(TestCase):
    """
    服务器信息模型测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.idc = IDC.objects.create(
            idc_name='测试机房',
            idc_code='TEST-IDC-001'
        )
        self.server = Server.objects.create(
            server_name='测试服务器',
            server_ip='192.168.1.100',
            server_inner_ip='10.0.0.1',
            server_port=22,
            server_username='root',
            idc=self.idc,
            server_cpu='4核',
            server_memory='8GB',
            server_disk='100GB',
            server_os='Linux',
            server_status=1,
            server_role='web'
        )
    
    def test_server_creation(self):
        """
        测试服务器创建
        """
        self.assertEqual(self.server.server_name, '测试服务器')
        self.assertEqual(self.server.server_ip, '192.168.1.100')
        self.assertEqual(self.server.idc.idc_name, '测试机房')
    
    def test_server_str(self):
        """
        测试服务器字符串表示
        """
        self.assertEqual(str(self.server), '测试服务器(192.168.1.100)')


class ProjectTestCase(TestCase):
    """
    项目信息模型测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.project = Project.objects.create(
            project_name='测试项目',
            project_code='TEST-PROJ-001',
            project_owner='张三',
            project_owner_display='张三',
            project_description='测试项目描述',
            project_priority=2,
            project_status=1
        )
    
    def test_project_creation(self):
        """
        测试项目创建
        """
        self.assertEqual(self.project.project_name, '测试项目')
        self.assertEqual(self.project.project_code, 'TEST-PROJ-001')
        self.assertEqual(self.project.project_priority, 2)
    
    def test_project_str(self):
        """
        测试项目字符串表示
        """
        self.assertEqual(str(self.project), '测试项目')


class ClusterTestCase(TestCase):
    """
    集群信息模型测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.project = Project.objects.create(
            project_name='测试项目',
            project_code='TEST-PROJ-001'
        )
        self.cluster = Cluster.objects.create(
            cluster_name='测试集群',
            cluster_code='TEST-CLUSTER-001',
            project=self.project,
            cluster_type='mysql',
            cluster_role='production',
            cluster_status=1
        )
    
    def test_cluster_creation(self):
        """
        测试集群创建
        """
        self.assertEqual(self.cluster.cluster_name, '测试集群')
        self.assertEqual(self.cluster.cluster_type, 'mysql')
        self.assertEqual(self.cluster.project.project_name, '测试项目')
    
    def test_cluster_str(self):
        """
        测试集群字符串表示
        """
        self.assertEqual(str(self.cluster), '测试集群')


class ResourceInstanceTestCase(TestCase):
    """
    实例资源关联模型测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.idc = IDC.objects.create(
            idc_name='测试机房',
            idc_code='TEST-IDC-001'
        )
        self.project = Project.objects.create(
            project_name='测试项目',
            project_code='TEST-PROJ-001'
        )
        self.server = Server.objects.create(
            server_name='测试服务器',
            server_ip='192.168.1.100',
            idc=self.idc
        )
        self.cluster = Cluster.objects.create(
            cluster_name='测试集群',
            cluster_code='TEST-CLUSTER-001',
            project=self.project,
            cluster_type='mysql'
        )
        self.resource_instance = ResourceInstance.objects.create(
            instance_id=1,
            instance_name='test-instance',
            server=self.server,
            cluster=self.cluster,
            project=self.project,
            idc=self.idc,
            instance_env='prod',
            instance_level=1
        )
    
    def test_resource_instance_creation(self):
        """
        测试实例资源关联创建
        """
        self.assertEqual(self.resource_instance.instance_name, 'test-instance')
        self.assertEqual(self.resource_instance.instance_env, 'prod')
        self.assertEqual(self.resource_instance.instance_level, 1)
    
    def test_resource_instance_str(self):
        """
        测试实例资源关联字符串表示
        """
        self.assertEqual(str(self.resource_instance), 'test-instance 资源关联')


if __name__ == '__main__':
    unittest.main()
