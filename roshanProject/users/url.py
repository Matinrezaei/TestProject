from django.urls import path
from .views import *
from dj_rest_auth.views import LogoutView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login_user'),
    path('register/', CustomRegisterView.as_view(), name= "account_register"),
    path('token/logout/', LogoutView.as_view(), name='logout'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]