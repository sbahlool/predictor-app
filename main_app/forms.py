from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Schedule, Comment, Predictions

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control',}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control',}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control',}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control',}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password',}))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control', 'data-toggle': 'password', 'id': 'password', }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class GameweekView(forms.Form):
    game_week = forms.ChoiceField(choices=[(1, 'Gameweek 1'), (2, 'Gameweek 2'), (3, 'Gameweek 3')])

    def my_view(request):
      form = GameweekView(request.POST)

      if form.is_valid():
          game_week = form.cleaned_data['gameweek']

          data = Schedule.objects.filter(gameweek=game_week)

          context = {'data': data}

          return render(request, 'schedule_list.html', context)

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    team = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['avatar', 'team']


class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']

class PredictionForm(ModelForm):
  class Meta:
    model = Predictions
    fields = ['predhometeamscore', 'predawayteamscore']

