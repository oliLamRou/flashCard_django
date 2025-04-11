from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Preference

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['languageA', 'languageB', 'learnMode']