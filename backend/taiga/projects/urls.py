from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.projects_list, name='projects_list'),
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^(?P<project_id>\d+)/$', views.project_details, name='project_details'),
    url(r'^(?P<project_id>\d+)/edit/$', views.edit_project, name='edit_project'),
    url(r'^(?P<project_id>\d+)/timelogs/$', views.project_timelogs, name='project_timelogs'),
]
