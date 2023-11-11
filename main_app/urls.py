from django.urls import path
from . import views
from .views import profile, ChangePasswordView, RegisterView


urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('schedule', views.ScheduleList.as_view(), name='schedule_index'),
  # path('gameweek/', GameweekView.as_view(), name='gameweek'),
  path('accounts/profile/', profile, name='users-profile'),
  path('accounts/signup/', RegisterView.as_view(), name='signup'),
  path('password_change/', ChangePasswordView.as_view(), name='password_change'),

  path('thread/', views.CommentList.as_view(), name='thread'),
  path('thread/<int:user_id>/add_comment/', views.CommentCreate.as_view, name='add_comment'),
]