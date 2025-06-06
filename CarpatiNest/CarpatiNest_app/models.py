from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Mountain(models.Model):
    CATEGORY_CHOICES = [
        ('carpati_meridionali', 'Carpații Meridionali'),
        ('carpati_orientali', 'Carpații Orientali'),
        ('carpati_occidentali', 'Carpații Occidentali'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Nume munte')
    description = models.TextField(verbose_name='Descriere')
    altitude = models.IntegerField(verbose_name='Altitudine (m)')
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        verbose_name='Categorie',
        default='carpati_meridionali'
    )
    image = models.ImageField(upload_to='mountains/', verbose_name='Imagine', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Munte'
        verbose_name_plural = 'Munți'
        ordering = ['-altitude']  # Sort by altitude descending

class Refuge(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nume refugiu')
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE, related_name='refuges', verbose_name='Munte')
    description = models.TextField(verbose_name='Descriere', blank=True, null=True)
    altitude = models.IntegerField(verbose_name='Altitudine (m)', null=True, blank=True)
    image = models.ImageField(upload_to='refuges/', verbose_name='Imagine', null=True, blank=True)
    capacity = models.IntegerField(verbose_name='Capacitate', default=10)
    
    # Coordonate GPS pentru integrarea cu API-ul meteo
    latitude = models.FloatField(verbose_name='Latitudine', null=True, blank=True, 
                                help_text='Coordonata latitudine pentru refugiu')
    longitude = models.FloatField(verbose_name='Longitudine', null=True, blank=True,
                                 help_text='Coordonata longitudine pentru refugiu')

    def __str__(self):
        return f"{self.name} ({self.mountain.name})"

    class Meta:
        verbose_name = 'Refugiu'
        verbose_name_plural = 'Refugii'
        ordering = ['mountain', 'name']

    def get_available_spots(self, booking_date):
        """
        Calculează numărul de locuri disponibile pentru o anumită dată
        """
        # Calculează suma persoanelor din rezervări confirmate sau în așteptare pentru această dată
        bookings_for_date = Booking.objects.filter(
            refuge=self,
            booking_date=booking_date,
            status__in=['pending', 'confirmed']
        )
        
        reserved_spots = sum(booking.members_count for booking in bookings_for_date)
        available = self.capacity - reserved_spots
        
        # Asigură-te că nu returnează un număr negativ
        return max(0, available)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name='Utilizator')
    refuge = models.ForeignKey(Refuge, on_delete=models.CASCADE, related_name='bookings', verbose_name='Refugiu')
    booking_date = models.DateField(verbose_name='Data rezervării', default=date.today)
    members_count = models.IntegerField(verbose_name='Număr de membri', default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data creării')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'În așteptare'),
            ('confirmed', 'Confirmată'),
            ('canceled', 'Anulată')
        ],
        default='pending',
        verbose_name='Status'
    )
    notes = models.TextField(blank=True, null=True, verbose_name='Note')

    class Meta:
        verbose_name = 'Rezervare'
        verbose_name_plural = 'Rezervări'
        ordering = ['-created_at']

    def __str__(self):
        return f"Rezervare {self.refuge.name} - {self.user.username} ({self.booking_date})"

class RefugeImage(models.Model):
    refuge = models.ForeignKey('Refuge', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='refuge_images/', verbose_name='Imagine')
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name='Descriere imagine')

    class Meta:
        verbose_name = 'Imagine refugiu'
        verbose_name_plural = 'Imagini refugii'

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Nemulțumit'),
        (2, '2 - Satisfăcător'),
        (3, '3 - Bun'),
        (4, '4 - Foarte bun'),
        (5, '5 - Excelent')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Utilizator')
    refuge = models.ForeignKey('Refuge', on_delete=models.CASCADE, related_name='reviews', verbose_name='Refugiu')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Evaluare')
    comment = models.TextField(verbose_name='Comentariu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data creării')
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Review {self.refuge.name} - {self.user.username} ({self.rating}/5)"