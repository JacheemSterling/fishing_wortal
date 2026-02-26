from django import forms
from django.contrib.auth.models import User
from .models import Profil

        
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        field.widget.attrs.update({'class': 'form-control bg-dark text-white border-secondary'})

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['bio', 'miejscowosc', 'wiek', 'avatar', 'ulubiona_metoda']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-info', 'rows': 3}),
            'miejscowosc': forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-info'}),
            'wiek': forms.NumberInput(attrs={'class': 'form-control bg-dark text-light border-info'}),
            'ulubiona_metoda': forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-info'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control bg-dark text-light border-info'}),
        }