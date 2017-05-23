from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.timelogs_list, name='timelogs_list'),
    url(r'^add_timelog/$', views.add_timelog, name='add_timelog'),
    url(r'^(?P<timelog_id>\d+)/$', views.timelog_details, name='timelog_details'),
    url(r'^add/$', views.add_timelog, name='add_timelog'),
    url(r'^(?P<timelog_id>\d+)/edit/$', views.edit_timelog, name='edit_timelog'),
    url(r'^(?P<timelog_id>\d+)/delete/$', views.delete_timelog, name='delete_timelog'),
]