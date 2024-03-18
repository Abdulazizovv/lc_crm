from django.urls import path
from . import views

urlpatterns = [
    path('login/token/', views.TokenObtainPairView.as_view(), name='login'),
    path('signup/token/', views.UserRegistrationView.as_view(), name='signup'),
]