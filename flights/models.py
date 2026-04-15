from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3,unique=True)
    city = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.code} - ({self.city})'


class Flight(models.Model):
    origin = models.ForeignKey(Airport,models.CASCADE,related_name='departures')
    destination = models.ForeignKey(Airport,models.CASCADE,related_name='arrivals')
    duration = models.IntegerField()

    def __str__(self):
        return f'{self.origin} -> {self.destination} ({self.duration}min)'
    def is_valid_flight(self):
        return self.origin != self.destination and self.duration > 0
        
    
class Passenger(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    flights = models.ManyToManyField(Flight,blank=True,related_name='passengers')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
