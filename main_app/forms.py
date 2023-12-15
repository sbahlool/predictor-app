from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Schedule, Comment, Predictions, Teams

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control',}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control',}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control',}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control',}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password',}))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-control', 'data-toggle': 'password', 'id': 'password', }))
    team = forms.ModelChoiceField(queryset=Teams.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'team']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        # Check if a profile already exists for the user
        profile, created = Profile.objects.get_or_create(user=user)

        # Update the existing profile with the specified team
        profile.team = self.cleaned_data['team']
        profile.save()

        return user

class GameweekViewForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['gameweek']
    

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    team = forms.ModelChoiceField(queryset=Teams.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['avatar', 'team']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class PredictionsForm(forms.ModelForm):
    class Meta:
        model = Predictions
        fields = ['schedule', 'predhometeamscore', 'predawayteamscore']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize the label for the 'predhometeamscore' field
        self.fields['predhometeamscore'].label = 'Home Team Score'
        self.fields['predawayteamscore'].label = 'Away Team Score'



