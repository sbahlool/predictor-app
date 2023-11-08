from django.urls import path
from . import views
from .views import profile

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('accounts/profile/', profile, name='users-profile'),
  path('accounts/signup/', views.signup, name='signup'),
]