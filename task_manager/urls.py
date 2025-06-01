from rest_framework.routers import DefaultRouter

from task_manager.views import ProjectViewSet, TestCeleryViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('test_celery', TestCeleryViewSet, basename='test_celery')
urlpatterns = [

              ] + router.urls
