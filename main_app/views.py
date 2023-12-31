from django.shortcuts import render, redirect, get_object_or_404
from .models import Schedule, Predictions, Comment, Profile
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.views import View
from django import forms
import datetime
from extra_views import CreateWithInlinesView, InlineFormSetFactory

from .forms import UpdateUserForm, UpdateProfileForm, RegisterForm, CommentForm, PredictionsForm


# Create your views here.
def home(request):
  return render(request, 'index.html')

def about(request):
  return render(request, 'about.html')

# def ranking(request):
#   return render(request, 'ranking_list.html')

def ranking_index(request):
    rankings = Profile.objects.all()
    return render(request, 'ranking_list.html', {'rankings': rankings})



### SCHEDULE
class ScheduleList(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'schedule_list.html'

    def get_queryset(self):
        gameweek = self.request.GET.get('gameweek', 1)
        return Schedule.objects.filter(gameweek=gameweek)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get distinct gameweeks and sort them in descending order
        gameweeks = Schedule.objects.values_list('gameweek', flat=True).distinct()
        context['gameweeks'] = sorted(gameweeks, reverse=False)

        # Set the selected gameweek
        context['selected_gameweek'] = int(self.request.GET.get('gameweek', 1))
        return context


class ScheduleDetail(LoginRequiredMixin, DetailView):
  model = Schedule

class ScheduleCreate(LoginRequiredMixin, CreateView):
  model = Schedule
  fields = ['gameweek', 'date', 'time', 'hometeam', 'awayteam']
  success_url = '/schedule/'

class ScheduleUpdate(LoginRequiredMixin, UpdateView):
  model = Schedule
  fields = ['hometeam','hometeamscore','awayteam','awayteamscore', 'match_completed']
  success_url = '/schedule/'

class ScheduleDelete(LoginRequiredMixin, DeleteView):
  model = Schedule
  success_url = '/schedule/'
  
#### PREDICTIONS
class PredictionsList(LoginRequiredMixin, ListView):
  model = Predictions

class PredictionsCreate(LoginRequiredMixin, CreateView):
    model = Predictions
    form_class = PredictionsForm
    template_name = 'predictions_form.html'
    success_url = '/schedule/'

    def get_context_data(self, **kwargs):
        print("test")
        context = super().get_context_data(**kwargs)
        # context['selectedSchedule'] = Schedule.objects.all().filter(id = self.kwargs['pk'])
        # print(context['selectedSchedule'])
        context["schedule"] = Schedule.objects.all().filter(id = self.kwargs['pk'])
        # print(context['schedule'])
        return context

    def form_valid(self, form):
        # print(schedule_id)
        schedule = form.cleaned_data['schedule']

        # Calculate the match time with the date and time from the schedule
        match_time = timezone.make_aware(
            timezone.datetime.combine(schedule.date, schedule.time)
        )

        # Calculate the restriction time (2 hours before the match)
        restriction_time = match_time - timezone.timedelta(hours=2)

        # Check if the current time is before the restriction time
        if timezone.now() >= restriction_time:
            messages.error(self.request, "Predictions are not allowed 2 hours before the match.")
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # print(self.kwargs['pk'])
        # print(form.fields['schedule'])
        form.fields['schedule'].queryset = Schedule.objects.all().filter(id = self.kwargs['pk'])
        form.fields['schedule'].empty_label = None
        # form['idd'] = self.kwargs['pk']
        # print(form)
        return form

### COMMENT
class CommentList(LoginRequiredMixin, ListView):
  model = Comment

class CommentCreate(LoginRequiredMixin, CreateView):
  model = Comment
  fields = ['comment']
  success_url = '/comment/'


  def form_valid(self, form):
    form.instance.user = self.request.user
    form.instance.timestamp = datetime.datetime.now()
    return super().form_valid(form)
  

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'comment_form.html'  # Replace with your actual template name
    success_url = '/comment/'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.edited = True  # Set the 'edited' field to True
        comment.save()
        return redirect(self.success_url)

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if comment.user != self.request.user:
            # Ensure that only the owner of the comment can edit it
            raise PermissionDenied
        return comment

class CommentDelete(LoginRequiredMixin, DeleteView):
  model = Comment
  success_url = '/comment/'


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

#### PROFILE

class ProfileView(ListView):
  model = Profile

class UserPredictionsView(TemplateView):
    template_name = 'user_predictions.html'


    # def get_queryset(self):
    #     gameweek = self.request.GET.get('gameweek', 1)
    #     return Schedule.objects.filter(gameweek=gameweek)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        
    #     # Get distinct gameweeks and sort them in descending order
    #     gameweeks = Schedule.objects.values_list('gameweek', flat=True).distinct()
    #     context['gameweeks'] = sorted(gameweeks, reverse=False)

    #     # Set the selected gameweek
    #     context['selected_gameweek'] = int(self.request.GET.get('gameweek', 1))
    #     return context

    def get_queryset(self):
        gameweek = self.request.GET.get('gameweek', 1)
        return Predictions.objects.filter(user=self.request.user, schedule__gameweek=gameweek)

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      # Get distinct gameweeks and sort them in ascending order
      gameweeks = sorted(Schedule.objects.values_list('gameweek', flat=True).distinct())

      # Set the selected gameweek
      selected_gameweek = int(self.request.GET.get('gameweek', 1))

      predictions = Predictions.objects.filter(
          user=self.request.user,
          schedule__gameweek=selected_gameweek
      )

      # Add the gameweeks and selected_gameweek to the context
      context['predictions'] = predictions
      context['selected_gameweek'] = selected_gameweek
      context['gameweeks'] = gameweeks

      return context
        

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile-view')  # Redirect to the user's profile page after successful update
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'update_profile.html', {'user_form': user_form, 'profile_form': profile_form})

