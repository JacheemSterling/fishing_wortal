from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import Polow, Komentarz, Like, Powiadomienie
from .forms import ProfilForm
from main.forms import KomentarzForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # To stworzy użytkownika (a sygnały stworzą profil!)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto stworzone dla {username}! Możesz się zalogować.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Witaj ponownie, {username}!')
                return redirect('index') 
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profil(request):
    from main.models import Polow 
    ryby = Polow.objects.filter(uzytkownik=request.user).order_by('-data_polowu')
    
    context = {
        'uzytkownik': request.user,
        'ryby': ryby,
        'liczba_ryb': ryby.count(),
        'najwieksza': ryby.order_by('-dlugosc_ryby').first(),
    }
    return render(request, 'users/profil.html', context)

@login_required
def edytuj_profil(request):
    profil = request.user.profil

    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profil) 
        if form.is_valid():
            form.save() 
            messages.success(request, "Twój profil został zaktualizowany!")
            return redirect('profil_publiczny', username=request.user.username) 
    else:
        form = ProfilForm(instance=request.user) 
    
    return render(request, 'users/edytuj_profil.html', {'form': form}) #

@login_required
def feed(request):
    wszystkie_polowy = Polow.objects.all().order_by('-data_polowu')
    filtr = request.GET.get('filter')

    if filtr == 'following' and request.user.is_authenticated:
        obserwowani_profile = request.user.profil.obserwuje.all()
        obserwowani_uzytkownicy = [p.user for p in obserwowani_profile]
        wszystkie_polowy = wszystkie_polowy.filter(uzytkownik__in=obserwowani_uzytkownicy)
                               

    polubione_id = []
    if request.user.is_authenticated:
        polubione_id = list(Like.objects.filter(uzytkownik=request.user).values_list('polow_id', flat=True))
    
    if request.method == 'POST':
        form = KomentarzForm(request.POST)
        if form.is_valid():
            nowy_komentarz = form.save(commit=False)
            nowy_komentarz.autor = request.user
            polow_id = request.POST.get('polow_id')
            nowy_komentarz.polow = Polow.objects.get(id=polow_id)
            nowy_komentarz.save()
            return redirect('feed')
    else:
        form = KomentarzForm()

    context = {
        'polowy': wszystkie_polowy,
        'filtr': filtr,
        'form': form,
        'polubione_id': polubione_id,
    }
    return render(request, 'main/feed.html', context)

@login_required
def usun_komentarz(request, pk):
    komentarz = get_object_or_404(Komentarz, pk=pk)
    if komentarz.autor == request.user:
        komentarz.delete()
        messages.success(request, "Komentarz został usunięty.")
    else:
        messages.error(request, "Nie masz uprawnień do usunięcia tego komentarza.")
    return redirect('feed')

@login_required
def obserwuj_uzytkownika(request, username):
    osoba_do_obserwowania = get_object_or_404(User, username=username)
    moj_profil = request.user.profil
    if osoba_do_obserwowania != request.user:
        if moj_profil.obserwuje.filter(id=osoba_do_obserwowania.profil.id).exists():
            moj_profil.obserwuje.remove(osoba_do_obserwowania.profil)
        else:
            moj_profil.obserwuje.add(osoba_do_obserwowania.profil)

            Powiadomienie.objects.create(
                odbiorca=osoba_do_obserwowania,
                nadawca=request.user,
                typ='obserwacja'
            )
    return redirect('profil_publiczny', username=username)