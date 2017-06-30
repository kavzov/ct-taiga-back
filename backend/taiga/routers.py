from rest_framework import routers
from taiga.users.views import UserViewSet
from taiga.projects.views import ProjectViewSet
from taiga.projects.issues.views import IssueViewSet
from taiga.timelogs.views import TimelogViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'users/(?P<user_id>\d+)/timelogs', TimelogViewSet, base_name='user-timelogs')
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'issues', IssueViewSet, base_name='issues')
router.register(r'issues/(?P<issue_id>\d+)/timelogs', TimelogViewSet, base_name='issue-timelogs')
