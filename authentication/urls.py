from django.urls import path
from . views import UserRegistrationView
# from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name='authentication'

urlpatterns =[
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-registration',UserRegistrationView.as_view(),name='user-registartion'),
]