from django.urls import path
from . import views
from users import views as users_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dodaj-polow/', views.dodaj_polow, name='dodaj_polow'),
    path('edytuj-polow/<int:pk>/', views.edytuj_polow, name='edytuj_polow'),
    path('usun-polow/<int:pk>/', views.usun_polow, name='usun_polow'),
    path('lista-polowow/', views.lista_polowow, name='lista_polowow'), 
    path('mapa/', views.mapa_lowisk, name='mapa_lowisk'),
    path('polub-polow/<int:pk>/', views.polub_polow, name='polub_polow'),
    path('profil/edytuj/', users_views.edytuj_profil, name='edytuj_profil'),
    path('profil/<str:username>/', views.profil_publiczny, name='profil_publiczny'),
    path('komentarz/usun/<int:pk>/', users_views.usun_komentarz, name='usun_komentarz'),
]