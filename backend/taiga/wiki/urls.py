from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.wiki_list, name='wiki_list'),
    url(r'^(?P<wiki_id>\d+)/$', views.wiki_details, name='wiki_details'),
    # url(r'^add/$', views.add_wiki, name='add_wiki'),
    url(r'^(?P<wiki_id>\d+)/edit/$', views.edit_wiki, name='edit_wiki'),
    url(r'^(?P<wiki_id>\d+)/delete/$', views.delete_wiki, name='delete_wiki'),
]