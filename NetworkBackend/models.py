from django.db import models

class Train(models.Model):
    train_number = models.CharField(max_length=10, unique=True)
    company = models.CharField(max_length=100)
    train_type = models.CharField(max_length=20)

class Station(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.city}"

class Cursa(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, default='Activ')

    def __str__(self):
        return f"{self.train.train_number} - {self.date} - {self.status}"

class Stop(models.Model):
    cursa = models.ForeignKey(Cursa, on_delete=models.CASCADE)
    
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    
    arrival_time = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)

    sequence_number = models.PositiveIntegerField()

    delay_minutes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['cursa', 'sequence_number']

    def __str__(self):
        return f"{self.cursa.train.train_number} - {self.station.name} - {self.arrival_time} - {self.departure_time}"
