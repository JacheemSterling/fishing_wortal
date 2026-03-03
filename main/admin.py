from django.contrib import admin
from .models import Lowisko, Polow, Like, Powiadomienie, Wiadomosc, Komentarz 

admin.site.register(Lowisko)
admin.site.register(Polow)
admin.site.register(Like)
admin.site.register(Komentarz)
admin.site.register(Wiadomosc)
admin.site.register(Powiadomienie)