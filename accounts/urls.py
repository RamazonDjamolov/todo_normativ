from accounts import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter


from accounts.views import ListUsersView

router = DefaultRouter()
router.register('users', ListUsersView, )

urlpatterns = [
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('register/', views.RegisterApiview.as_view(), name='register'),
                  path('update/<int:pk>/', views.UpdateView.as_view(), name='update'),
                  # path('', ListUsersView.as_view(), name='list'),
              ] + router.urls
