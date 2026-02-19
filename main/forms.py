from django import forms
from .models import Polow, User, Komentarz

class PolowForm(forms.ModelForm):
    class Meta:
        model = Polow
        fields = ['gatunek_ryby', 'waga_ryby', 'dlugosc_ryby', 'lowisko', 'zdjecie_ryby', 'opis']
        widgets = {
            'opis': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Jakieś szczegóły wyprawy?'}),
        }

class EdycjaProfiluForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Adres e-mail',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control bg-dark text-white border-secondary'})

class KomentarzForm(forms.ModelForm):
    class Meta:
        model = Komentarz
        fields = ['tresc']
        widgets = {
            'tresc': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Napisz coś o tym połowie...',
                'rows': 2
            }),
        }
        labels = {'tresc': ''}