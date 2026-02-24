from django.urls import path
from .views import (
    RegisterView,
    CurrentUserView,
    CustomerLoginView,
    AdminRecentActionsView,
    AdminClearRecentActionsView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('customer-login/', CustomerLoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('me/', CurrentUserView.as_view()),
    path('admin-actions/', AdminRecentActionsView.as_view()),
    path('admin-actions/clear/', AdminClearRecentActionsView.as_view()),
]
