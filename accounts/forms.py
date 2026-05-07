from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('mentor', 'Mentor'), ('user', 'User')], initial='user')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'role')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
