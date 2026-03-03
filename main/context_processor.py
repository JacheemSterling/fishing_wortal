from .models import Wiadomosc, Powiadomienie

def powiadomienia_systemowe(request):
    if request.user.is_authenticated:
        n_wiadomosci = Wiadomosc.objects.filter(odbiorca=request.user, czy_przeczytana=False).count()
        n_obserwujacy = Powiadomienie.objects.filter(odbiorca=request.user, czy_przeczytane=False).count()
        
        return {
            'nieprzeczytane_count': n_wiadomosci, 
            'n_obserwujacy': n_obserwujacy,       
            'suma_powiadomien': n_wiadomosci + n_obserwujacy
        }
    return {'nieprzeczytane_count': 0, 'n_obserwujacy': 0, 'suma_powiadomien': 0}