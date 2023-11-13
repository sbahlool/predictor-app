from django.shortcuts import render, redirect
from .models import Schedule, Predictions, Comment, Ranking
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django import forms
import datetime
from extra_views import CreateWithInlinesView, InlineFormSetFactory

from .forms import UpdateUserForm, UpdateProfileForm, RegisterForm, CommentForm


# Create your views here.
def home(request):
  return render(request, 'index.html')

def about(request):
  return render(request, 'about.html')


# def schedule_index(request):
#   schedule = Schedule.objects.all()
#   return render(request, 'schedule.html', {'schedule': schedule})

class ScheduleList(ListView):
  model = Schedule

class ScheduleDetail(DetailView):
  model = Schedule

class ScheduleCreate(CreateView):
  model = Schedule
  fields = ['gameweek', 'date', 'time', 'hometeam', 'awayteam']
  success_url = '/schedule/'
  

class PredictionsList(ListView):
  model = Predictions

class PredictionsCreate(CreateView):
  model = Predictions
  fields = ['schedule']
  success_url = '/schedule/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


######################
# class PredictionsCreate(InlineFormSetFactory):
#   model = Predictions
#   fields = ['predhometeamscore','predawayteamscore']

# class SchedulePrediction(CreateWithInlinesView):
#   model = Schedule
#   inlines = [PredictionsCreate]
#   fields = ['hometeam','awayteam']
#   template_name = 'prediction_schedule.html'
#######################

  


class CommentList(ListView):
  model = Comment

class CommentCreate(LoginRequiredMixin, CreateView):
  model = Comment
  fields = ['comment']
  success_url = '/comment/'


  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.timestamp = datetime.datetime.now()
    return super().form_valid(form)
  

class CommentUpdate(UpdateView):
  model = Comment
  fields = ['comment']
  success_url = '/comment/'

class CommentDelete(DeleteView):
  model = Comment
  success_url = '/comment/'

class RankingList(ListView):
  model = Ranking



class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})

# def signup(request):
#   error_message = ''
#   if request.method == 'POST':
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#       user = form.save()
#       login(request, user)
#       return redirect('/')
#     else:
#       error_message = 'Invalid Signup', form.error_messages
    
#   form = UserCreationForm()
#   context = {'form': form, 'error message': error_message}
#   return render(request, 'registration/signup.html', context)