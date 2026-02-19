import json
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Polow, Lowisko, Like
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from .forms import PolowForm, EdycjaProfiluForm

def profil_publiczny(request, username):
    # Szukamy konkretnego wędkarza po nazwie użytkownika
    wedkarz = get_object_or_404(User, username=username)
    # Pobieramy wszystkie jego połowy, od najnowszych
    ryby_wedkarza = Polow.objects.filter(uzytkownik=wedkarz).order_by('-data_polowu')
    
    # Dodatkowe statystyki dla efektu "wow"
    liczba_ryb = ryby_wedkarza.count()
    najwieksza_ryba = ryby_wedkarza.order_by('-dlugosc_ryby').first()

    context = {
        'wedkarz': wedkarz,
        'ryby': ryby_wedkarza,
        'liczba_ryb': liczba_ryb,
        'najwieksza': najwieksza_ryba,
    }
    return render(request, 'main/profil_publiczny.html', context)


@login_required
def dodaj_polow(request):
    if request.method == 'POST':
        form = PolowForm(request.POST, request.FILES)
        if form.is_valid():
            polow = form.save(commit=False)
            polow.uzytkownik = request.user
            polow.save()
            return redirect('index')
    else:
        form = PolowForm()
    
    return render(request, 'main/dodaj_polow.html', {'form': form})

@login_required
def edytuj_polow(request, pk):
    polow = get_object_or_404(Polow, pk=pk, uzytkownik = request.user)
    if request.method == "POST":
        form = PolowForm(request.POST, request.FILES, instance=polow)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PolowForm(instance=polow)
    return render(request, 'main/dodaj_polow.html', {'form': form})

@login_required
def usun_polow(request, pk):
    polow = get_object_or_404(Polow, pk=pk, uzytkownik = request.user)
    if request.method == "POST":
        polow.delete()
        return redirect('index')
    return render(request, 'main/usun_potwierdzenie.html', {'polow': polow})

@login_required
def index(request):
    moje_polowy = Polow.objects.filter(uzytkownik=request.user)
    liczba_ryb = moje_polowy.count()
    laczna_waga = moje_polowy.aggregate(Sum('waga_ryby'))['waga_ryby__sum'] or 0
    dane_wykresu = moje_polowy.values('gatunek_ryby').annotate(total=Count('gatunek_ryby'))

    ostatnie_polowy = moje_polowy.order_by('-data_polowu')[:3]
    
    context = {
        'liczba_ryb': liczba_ryb,
        'laczna_waga': laczna_waga,
        'dane_wykresu': dane_wykresu, 
        'ostatnie_polowy': ostatnie_polowy,
    }
    
    return render(request, 'main/index.html', context)

def lista_polowow(request):
    polowy = Polow.objects.filter(uzytkownik=request.user).order_by('-data_polowu')
    return render(request, 'main/lista_polowow.html', {'polowy': polowy})

def mapa_lowisk(request):
    lowiska_qs = Lowisko.objects.all()
    lowiska_data = []
    for l in lowiska_qs:
        lowiska_data.append({
            'id': l.id,
            'nazwa': l.nazwa,
            'miejscowosc': l.miejscowosc,
            'lat': l.lat,
            'lon': l.lon,   
        })
    lowiska_json = json.dumps(lowiska_data)

    return render(request, 'main/mapa.html', {         
    'lowiska_json': lowiska_json,
    'lowiska_list': lowiska_qs
    })



@login_required
def polub_polow(request, pk):
    polow = get_object_or_404(Polow, pk=pk)
    polubienie, created = Like.objects.get_or_create(uzytkownik=request.user, polow=polow)

    if not created:
        polubienie.delete()

    return redirect('feed')
    