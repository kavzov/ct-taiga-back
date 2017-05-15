from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.users_list, name='userinfo'),
    url(r'^(?P<user_id>\d+)/$', views.user_details, name='userinfo'),
]