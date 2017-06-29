from django.conf.urls import url
from . import views
from taiga.timelogs.views import view_timelogs


urlpatterns = [
    url(r'^$', views.UsersList.as_view(), name='users-list'),
    # url(r'^$', views.users_list, name='users_list'),

    url(r'^(?P<pk>\d+)/$', views.UserDetails.as_view(), name='user_details'),
    # url(r'^(?P<user_id>\d+)/$', views.user_details, name='user_details'),

    url(r'^(?P<user_id>\d+)/timelogs/$', view_timelogs, name='user_timelogs'),
]

# users_list = views.UserViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# user_detail = views.UserViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
