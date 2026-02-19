from django.db import models
from django.contrib.auth.models import User

class Lowisko(models.Model):
    nazwa = models.CharField(max_length=200, verbose_name="Nazwa łowiska")
    lat = models.FloatField(verbose_name="szerokość geograficzna (Lat)", default=52.4)
    lon = models.FloatField(verbose_name="długość geograficzna (Lon)", default=21.0)
    miejscowosc = models.CharField(max_length=100, verbose_name="Miejscowość")

    class Meta:
        verbose_name = "Łowisko"
        verbose_name_plural = "Łowiska"

    def __str__(self):
        return self.nazwa

class Polow(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polowy')
    lowisko = models.ForeignKey(Lowisko, on_delete=models.SET_NULL, null=True, verbose_name="Miejsce połowu")
    gatunek_ryby = models.CharField(max_length=90, verbose_name="Gatunek ryby")
    waga_ryby = models.DecimalField(max_digits=6, decimal_places=2, help_text="kg", null=True, blank=True)
    dlugosc_ryby = models.PositiveIntegerField(help_text="cm", null=True, blank=True)
    data_polowu = models.DateTimeField(auto_now_add=True)
    zdjecie_ryby = models.ImageField(upload_to='zdjecia_ryb/', null=True, blank=True)
    opis = models.TextField(blank=True, verbose_name="Dodatkowe informacje")

    class Meta:
        verbose_name = "Połów"
        verbose_name_plural = "Połowy"

    def czy_polubione_przez(self,user):
        return self.likes.filter(uzytkownik=user).exists()

    def __str__(self):
        return f"{self.gatunek_ryby} ({self.data_polowu.strftime('%d.%m.%Y')})"
    
class Komentarz(models.Model):
    polow = models.ForeignKey(Polow, on_delete=models.CASCADE, related_name='komentarze')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='komenatrze')
    tresc = models.TextField(verbose_name="Treść komentarza")
    data_dodania = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"

class Like(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    related_name='likes'
    polow = models.ForeignKey(Polow, on_delete=models.CASCADE, related_name='likes') 
    data_polubienia = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('uzytkownik', 'polow')