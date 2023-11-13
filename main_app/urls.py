from django.urls import path
from . import views
from .views import profile, ChangePasswordView, RegisterView


urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('schedule/', views.ScheduleList.as_view(), name='schedule_index'),
  path('schedule/create/', views.ScheduleCreate.as_view(), name='schedule_create'),
  # path('gameweek/', GameweekView.as_view(), name='gameweek'),
  path('accounts/profile/', profile, name='users-profile'),
  path('accounts/signup/', RegisterView.as_view(), name='signup'),
  path('password_change/', ChangePasswordView.as_view(), name='password_change'),

  path('comment/', views.CommentList.as_view(), name='comment'),
  path('comment/create', views.CommentCreate.as_view(), name='comment_create'),
  path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
  path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),

  path('schedule/<int:pk>', views.ScheduleDetail.as_view(), name='schedule_detail'),
  path('prediction/<int:pk>', views.PredictionsList.as_view(), name='prediction_detail'),

  path('schedule/<int:pk>/prediction/', views.PredictionsCreate.as_view(), name='prediction_create'),
  # path('schedule/<int:pk>/prediction/', views.SchedulePrediction.as_view(), name='prediction_create'),

  path('ranking/', views.RankingList.as_view(), name ="ranking_index")
]