from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.auth_login, name='auth_login'),
    url(r'^logout/$', views.auth_logout, name='auth_logout'),
    url(r'^test/$', views.test, name='test'),
    url(r'^search/$', views.search, name='search'),
    url(r'^testformset/$', views.testformset, name='testformset'),
]
