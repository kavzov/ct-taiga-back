from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.users_list, name='users_list'),
    url(r'^(?P<user_id>\d+)/$', views.user_details, name='user_details'),
    url(r'^(?P<user_id>\d+)/timelogs/$', views.user_timelogs, name='user_timelogs'),
]