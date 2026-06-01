# -*- coding: UTF-8 -*-
from rest_framework import serializers
from resource_management.models import ResourceGroup, Instance, Users


class ResourceGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceGroup
        fields = '__all__'


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'display', 'email', 'resource_group']
