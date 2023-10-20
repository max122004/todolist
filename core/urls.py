from django.urls import re_path, path, include
from django.contrib import admin
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import UserCreateAPIView, Logout, UserRetrieveUpdateAPIView, PasswordUpdateAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view()),
    path('login/', views.obtain_auth_token),
    path('profile/', UserRetrieveUpdateAPIView.as_view()),
    path('update_password/', PasswordUpdateAPIView.as_view()),
    path('logout/', Logout.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]