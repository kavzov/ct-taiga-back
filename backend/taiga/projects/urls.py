from django.conf.urls import url
from . import views
from .issues import views as issues_views
from taiga.timelogs.views import view_timelogs

urlpatterns = [
    url(r'^$', views.projects_list, name='projects_list'),
    url(r'^add/$', views.add_project, name='add_project'),
    url(r'^(?P<project_id>\d+)/$', views.project_details, name='project_details'),
    url(r'^(?P<project_id>\d+)/edit/$', views.edit_project, name='edit_project'),
    url(r'^(?P<project_id>\d+)/delete/$', views.delete_project, name='delete_project'),
    url(r'^(?P<project_id>\d+)/add_issue/$', issues_views.add_issue, name='add_issue'),
    # url(r'^(?P<project_id>\d+)/timelogs/$', views.project_timelogs, name='project_timelogs'),
    url(r'^(?P<project_id>\d+)/timelogs/$', view_timelogs, name='project_timelogs'),
]
