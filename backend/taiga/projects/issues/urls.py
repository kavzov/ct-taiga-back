from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.issues_list, name='issues_list'),
    url(r'^add_issue/$', views.add_issue, name='add_issue'),
    url(r'^(?P<issue_id>\d+)/$', views.issue_details, name='issue_details'),
    url(r'^(?P<issue_id>\d+)/timelogs$', views.issue_timelogs, name='issue_tmelogs'),
]