from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.
def home(request):
  return render(request, 'index.html')

def about(request):
  return render(request, 'about.html')

@login_required
def profile(request):
  return render(request, 'profile.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid Signup', form.error_messages
    
  form = UserCreationForm()
  context = {'form': form, 'error message': error_message}
  return render(request, 'registration/signup.html', context)