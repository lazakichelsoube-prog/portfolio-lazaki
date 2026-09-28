from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ClientViewSet,
    EtapeViewSet,
    MessageViewSet,
    ProfileView,
    ProjectViewSet,
    SkillViewSet,
)

router = DefaultRouter()
router.register('skills', SkillViewSet, basename='skill')
router.register('projects', ProjectViewSet, basename='project')
router.register('clients', ClientViewSet, basename='client')
router.register('etapes', EtapeViewSet, basename='etape')
router.register('messages', MessageViewSet, basename='message')

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]