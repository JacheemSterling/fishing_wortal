from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    obserwuje = models.ManyToManyField('self', related_name="obserwujacy", symmetrical=False, blank=True)
    bio = models.TextField(blank=True, verbose_name="O mnie / Osiągnięcia")
    ulubiona_metoda = models.CharField(max_length=100, blank=True, verbose_name="Ulubiona metoda")
    miejscowosc = models.CharField(max_length=100, blank=True, verbose_name="Miejscowość")
    wiek = models.IntegerField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(10), MaxValueValidator(100)],
        verbose_name="Wiek"
    )
    avatar = models.ImageField(upload_to='avatars/', default='default.jpg')
    data_dolaczenia = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Profil użytkownika {self.user.username}"