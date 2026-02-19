from django import forms
from django.contrib.auth.models import User
from .models import Profil

class EdycjaProfiluForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        field.widget.attrs.update({'class': 'form-control bg-dark text-white border-secondary'})