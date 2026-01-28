from django import forms
from django.contrib.auth.models import User
from .models import Profil

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['miejscowosc', 'wiek', 'bio', 'avatar']