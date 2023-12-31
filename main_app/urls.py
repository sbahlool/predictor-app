from django.urls import path
from . import views
from .views import profile, ChangePasswordView, RegisterView


urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('ranking/', views.ranking_index, name='ranking_index'),
  path('schedule/', views.ScheduleList.as_view(), name='schedule_index'),
  path('schedule/create/', views.ScheduleCreate.as_view(), name='schedule_create'),
  path('schedule/<int:pk>/update/', views.ScheduleUpdate.as_view(), name='schedule_update'),
  path('schedule/<int:pk>/delete/', views.ScheduleDelete.as_view(), name='schedule_delete'),

  path('accounts/profileview', views.ProfileView.as_view(), name='profile-view'),
  path('accounts/profile/', profile, name='users-profile'),
  path('accounts/signup/', RegisterView.as_view(), name='signup'),
  path('password_change/', ChangePasswordView.as_view(), name='password_change'),

  path('comment/', views.CommentList.as_view(), name='comment'),
  path('comment/create', views.CommentCreate.as_view(), name='comment_create'),
  path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
  path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),

  path('schedule/<int:pk>', views.ScheduleDetail.as_view(), name='schedule_detail'),
  path('prediction/<int:pk>', views.PredictionsList.as_view(), name='prediction_detail'),
  path('my-predictions/', views.UserPredictionsView.as_view(), name='user-predictions'),

  path('schedule/<int:pk>/prediction/', views.PredictionsCreate.as_view(), name='prediction_create'),

]