from django.contrib import admin
from .models import Lowisko, Polow, Like # Importujemy Twoje modele

# Rejestrujemy modele, aby pojawiły się w panelu admina
admin.site.register(Lowisko)
admin.site.register(Polow)
admin.site.register(Like)