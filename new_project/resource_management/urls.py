# -*- coding: UTF-8 -*-
from django.urls import path
from resource_management import views

app_name = 'resource_management'

urlpatterns = [
    path('group/', views.group, name='group'),
    path('associated-objects/', views.associated_objects, name='associated_objects'),
    path('unassociated-objects/', views.unassociated_objects, name='unassociated_objects'),
    path('instances/', views.instances, name='instances'),
    path('user-all-instances/', views.user_all_instances, name='user_all_instances'),
    path('addrelation/', views.addrelation, name='addrelation'),
    path('auditors/', views.auditors, name='auditors'),
    path('changeauditors/', views.changeauditors, name='changeauditors'),
]
