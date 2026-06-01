# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.forms import PasswordInput

from .models import IDC, Server, Project, Cluster, ResourceInstance


@admin.register(IDC)
class IDCAdmin(admin.ModelAdmin):
    list_display = ('idc_id', 'idc_name', 'idc_code', 'idc_address', 'idc_status', 'create_time')
    search_fields = ('idc_name', 'idc_code', 'idc_address')
    list_filter = ('idc_status',)
    list_display_links = ('idc_id', 'idc_name')


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('server_id', 'server_name', 'server_ip', 'idc', 'server_status', 'create_time')
    search_fields = ('server_name', 'server_ip', 'server_inner_ip')
    list_filter = ('idc', 'server_status')
    list_display_links = ('server_id', 'server_name')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'server_password':
            kwargs['widget'] = PasswordInput(render_value=True)
        return super(ServerAdmin, self).formfield_for_dbfield(db_field, **kwargs)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_name', 'project_code', 'project_owner', 'project_priority', 'project_status', 'create_time')
    search_fields = ('project_name', 'project_code', 'project_owner')
    list_filter = ('project_status', 'project_priority')
    list_display_links = ('project_id', 'project_name')


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('cluster_id', 'cluster_name', 'cluster_code', 'project', 'cluster_type', 'cluster_role', 'cluster_status', 'create_time')
    search_fields = ('cluster_name', 'cluster_code')
    list_filter = ('project', 'cluster_type', 'cluster_role', 'cluster_status')
    list_display_links = ('cluster_id', 'cluster_name')
    filter_horizontal = ('servers',)


@admin.register(ResourceInstance)
class ResourceInstanceAdmin(admin.ModelAdmin):
    list_display = ('resource_instance_id', 'instance_name', 'server', 'cluster', 'project', 'idc', 'instance_env', 'instance_level')
    search_fields = ('instance_name',)
    list_filter = ('instance_env', 'instance_level', 'idc', 'project', 'cluster', 'server')
    list_display_links = ('resource_instance_id', 'instance_name')
