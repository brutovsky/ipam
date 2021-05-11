from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'users-api'
urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('users/register/', views.UserCreate.as_view(), name='user-create'),
    path('account/profile/', views.UserProfileDetail.as_view(), name='user_profile-detail'),
    path('account/change-password/', views.ChangePassword.as_view(), name='user_password-update'),
    path('groups/', views.GroupList.as_view(), name='group-list'),
    path('groups/<int:pk>/', views.GroupDetail.as_view(), name='group-detail'),
    path('token', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
