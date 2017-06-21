from django.conf.urls import url, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    url(r'^projects/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), name='project'),
    url(r'^pprojects/$', views.ProjectsList.as_view()),
    url(r'^project_edit/(?P<pk>[0-9]+)/$', views.ProjectEdit.as_view(), name='project-edit'),
    # url(r'^', include(router.urls)),
    # url(r'^project/(?P<pk>[0-9]+)$/', views.ProjectDetails.as_view()),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/$', views.auth_login, name='auth_login'),
    url(r'^logout/$', views.auth_logout, name='auth_logout'),
    url(r'^test/$', views.test, name='test'),
    url(r'^search/$', views.search, name='search'),
]

