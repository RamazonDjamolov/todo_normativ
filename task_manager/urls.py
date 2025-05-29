from rest_framework.routers import DefaultRouter

from task_manager.views import ProjectViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, )
urlpatterns = [

]+router.urls