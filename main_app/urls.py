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

  path('comment/', views.CommentList.as_view(), name='comment'),
  # path('thread/<int:comment_id>/add_comment', views.add_comment, name='add_comment'),
  path('comment/create', views.CommentCreate.as_view(), name='comment_create')
]