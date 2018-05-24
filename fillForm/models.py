from django.db import models
from django.utils import timezone

class Vehicle(models.Model):
    name = models.TextField(null=False)
    number = models.TextField(null=False, unique=True)

    def __str__(self):
        return "%s %s" % (self.number, self.name)

class Driver(models.Model):
    name = models.TextField(null=False)
    surname = models.TextField(null=False)

    def __str__(self):
        return "%s %s" % (self.name, self.surname)


class Form(models.Model):
    date = models.DateTimeField("filled date")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    odometer_before = models.IntegerField(null=False)
    odometer_after = models.IntegerField(null=False)
    fuel_given = models.FloatField(null=False)
    fuel_before = models.FloatField(null=False)
    fuel_after = models.FloatField(null=False)

    @classmethod
    def create(cls, date, vehicle, driver, odometer_before, odometer_after, fuel_given, fuel_before, fuel_after):
        form = cls(date = date, vehicle = vehicle, driver = driver,
                   odometer_before = odometer_before, odometer_after = odometer_after,
                   fuel_given = fuel_given, fuel_before = fuel_before, fuel_after = fuel_after)
        return form
