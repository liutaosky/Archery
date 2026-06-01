# -*- coding: UTF-8 -*-
from django.contrib import admin
from resource_management.models import ResourceGroup, Instance


@admin.register(ResourceGroup)
class ResourceGroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'group_name', 'group_parent_id', 'group_sort', 'group_level', 'is_deleted', 'create_time')
    list_filter = ('is_deleted', 'group_level')
    search_fields = ('group_name',)
    ordering = ('group_sort', 'group_id')


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ('instance_name', 'type', 'db_type', 'host', 'port', 'create_time')
    list_filter = ('type', 'db_type')
    search_fields = ('instance_name', 'host')
    ordering = ('instance_name',)
