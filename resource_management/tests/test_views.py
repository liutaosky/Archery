# -*- coding: UTF-8 -*-
"""
资源管理模块视图单元测试
"""
import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission

from resource_management.models import IDC, Server, Project, Cluster, ResourceInstance


class IDCViewTestCase(TestCase):
    """
    机房信息视图测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        IDC.objects.create(
            idc_name='测试机房',
            idc_code='TEST-IDC-001'
        )
    
    def test_idc_list_view(self):
        """
        测试机房列表视图
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('resource_management:idc_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试机房')


class ServerViewTestCase(TestCase):
    """
    服务器信息视图测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.idc = IDC.objects.create(
            idc_name='测试机房',
            idc_code='TEST-IDC-001'
        )
        Server.objects.create(
            server_name='测试服务器',
            server_ip='192.168.1.100',
            idc=self.idc
        )
    
    def test_server_list_view(self):
        """
        测试服务器列表视图
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('resource_management:server_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试服务器')


class ProjectViewTestCase(TestCase):
    """
    项目信息视图测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        Project.objects.create(
            project_name='测试项目',
            project_code='TEST-PROJ-001'
        )
    
    def test_project_list_view(self):
        """
        测试项目列表视图
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('resource_management:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试项目')


class ClusterViewTestCase(TestCase):
    """
    集群信息视图测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.project = Project.objects.create(
            project_name='测试项目',
            project_code='TEST-PROJ-001'
        )
        Cluster.objects.create(
            cluster_name='测试集群',
            cluster_code='TEST-CLUSTER-001',
            project=self.project,
            cluster_type='mysql'
        )
    
    def test_cluster_list_view(self):
        """
        测试集群列表视图
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('resource_management:cluster_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试集群')


class ResourceInstanceViewTestCase(TestCase):
    """
    实例资源关联视图测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
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
        ResourceInstance.objects.create(
            instance_id=1,
            instance_name='test-instance',
            server=self.server,
            cluster=self.cluster,
            project=self.project,
            idc=self.idc
        )
    
    def test_resource_instance_list_view(self):
        """
        测试实例资源关联列表视图
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('resource_management:resource_instance_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test-instance')


class APIViewTestCase(TestCase):
    """
    API接口视图测试
    """
    
    def setUp(self):
        """
        测试数据准备
        """
        self.client = Client()
        
        self.idc = IDC.objects.create(
            idc_name='测试机房',
            idc_code='TEST-IDC-001'
        )
        self.project = Project.objects.create(
            project_name='测试项目',
            project_code='TEST-PROJ-001'
        )
    
    def test_api_idc_list(self):
        """
        测试机房列表API
        """
        response = self.client.get(reverse('resource_management:api_idc_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 0)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], '测试机房')
    
    def test_api_project_list(self):
        """
        测试项目列表API
        """
        response = self.client.get(reverse('resource_management:api_project_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 0)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], '测试项目')


if __name__ == '__main__':
    unittest.main()
