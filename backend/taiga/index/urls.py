from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.auth_login, name='auth_login'),
    url(r'^logout/$', views.auth_logout, name='auth_logout'),
]
