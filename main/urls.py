from django.urls import path
from . import views
from users import views as users_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dodaj-polow/', views.dodaj_polow, name='dodaj_polow'),
    path('edytuj-polow/<int:pk>/', views.edytuj_polow, name='edytuj_polow'),
    path('usun-polow/<int:pk>/', views.usun_polow, name='usun_polow'),
    path('lista-polowow/', views.lista_polowow, name='lista_polowow'), 
    path('lowiska/', views.mapa_lowisk, name='mapa_lowisk'),
    path('polub-polow/<int:pk>/', views.polub_polow, name='polub_polow'),
    path('profil/edytuj/', users_views.edytuj_profil, name='edytuj_profil'),
    path('profil/<str:username>/', views.profil_publiczny, name='profil_publiczny'),
    path('komentarz/usun/<int:pk>/', users_views.usun_komentarz, name='usun_komentarz'),
    path('obserwuj/<str:username>/', users_views.obserwuj_uzytkownika, name='obserwuj_uzytkownika'),
    path('szukaj/', views.szukaj_wedkarzy, name='szukaj_wedkarzy'),
    path('wiadomosci/', views.lista_czatow, name='lista_czatow'),
    path('wiadomosci/<str:username>/', views.okno_czatu, name='okno_czatu'),
]