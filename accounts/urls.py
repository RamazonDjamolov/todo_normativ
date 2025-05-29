from accounts import views
from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views import ListUsersView

router = DefaultRouter()
router.register('users', ListUsersView, )

urlpatterns = [
                  path('register/', views.RegisterApiview.as_view(), name='register'),
                  path('update/<int:pk>/', views.UpdateView.as_view(), name='update'),
                  # path('', ListUsersView.as_view(), name='list'),
              ] + router.urls
