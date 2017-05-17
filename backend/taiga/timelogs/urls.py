from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.timelogs_list, name='timelogs_list'),
    url(r'^add_timelog/$', views.add_timelog, name='add_timelog'),
    url(r'^(?P<timelog_id>\d+)/$', views.timelog_details, name='timelog_details'),
]