from rest_framework import routers
from taiga.users.views import UserViewSet
from taiga.projects.views import ProjectViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'projects', ProjectViewSet, base_name='projects')
