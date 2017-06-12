from django.conf.urls import url
from . import views
from taiga.timelogs import views as timelogs_views


urlpatterns = [
    url(r'^$', views.issues_list, name='issues_list'),
    # url(r'^add_issue/$', views.add_issue, name='add_issue'),
    url(r'^(?P<issue_id>\d+)/$', views.issue_details, name='issue_details'),
    url(r'^(?P<issue_id>\d+)/edit/$', views.edit_issue, name='edit_issue'),
    url(r'^(?P<issue_id>\d+)/delete/$', views.delete_issue, name='delete_issue'),
    url(r'^(?P<issue_id>\d+)/timelogs/$', timelogs_views.view_timelogs, name='issue_timelogs'),
    url(r'^(?P<issue_id>\d+)/add_timelog/$', timelogs_views.add_timelog, name='add_timelog'),
]