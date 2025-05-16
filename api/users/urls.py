from django.urls import path
from .views import UserInfoView, UserRegistrationView, LoginView, LogoutView, CookieTokenRefreshView

urlpatterns = [
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]
