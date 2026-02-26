import json
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Polow, Lowisko, Like, Wiadomosc, Powiadomienie
from django.db.models import Sum, Count, Q
from django.contrib.auth.decorators import login_required
from .forms import PolowForm

def profil_publiczny(request, username):
    wedkarz = get_object_or_404(User, username=username)
    ryby_wedkarza = Polow.objects.filter(uzytkownik=wedkarz).order_by('-data_polowu')
    liczba_ryb = ryby_wedkarza.count()
    najwieksza_ryba = ryby_wedkarza.order_by('-dlugosc_ryby').first()
    wedkarz = get_object_or_404(User, username=username)

    if request.user == wedkarz:
        Powiadomienie.objects.filter(odbiorca=request.user, czy_przeczytane=False).update(czy_przeczytane=True)

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

@login_required
def lista_czatow(request):
    wiadomosci = Wiadomosc.objects.filter(Q(nadawca=request.user) | Q(odbiorca=request.user)).order_by('-data_wyslania')
    rozmowcy_id = set()
    for w in wiadomosci:
        rozmowcy_id.add(w.nadawca.id if w.odbiorca == request.user else w.odbiorca.id)

    rozmowcy = User.objects.filter(id__in=rozmowcy_id)
    return render(request, 'main/lista_czatow.html', {'rozmowcy': rozmowcy})

@login_required
def okno_czatu(request, username):
    rozmowca = get_object_or_404(User, username=username)
    Wiadomosc.objects.filter(nadawca=rozmowca, odbiorca=request.user, czy_przeczytana=False).update(czy_przeczytana=True)
    wiadomosci = Wiadomosc.objects.filter(
        (Q(nadawca=request.user) & Q(odbiorca=rozmowca)) |
        (Q(nadawca=rozmowca) & Q(odbiorca=request.user))
        ).order_by('data_wyslania')
    
    if request.method == 'POST':
        tresc = request.POST.get('tresc')
        if tresc:
            Wiadomosc.objects.create(nadawca=request.user, odbiorca=rozmowca, tresc=tresc)
            return redirect('okno_czatu', username=username)
        
    return render(request, 'main/okno_czatu.html', {
        'rozmowca': rozmowca,
        'wiadomosci': wiadomosci,
    })

@login_required 
def szukaj_wedkarzy(request):
    query = request.GET.get('q')
    wyniki = []
    if query:
        wyniki = User.objects.filter(Q(username__icontains=query)).exclude(id=request.user.id)
    return render(request, 'main/szukaj_uzytkownikow.html', {
        'wyniki': wyniki,
        'query': query,
    })

    