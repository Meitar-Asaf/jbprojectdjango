from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date
# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.country_name
    
def validate_date(start_date, end_date):
    if start_date <= date.today():
        raise ValidationError("Start date must be in the future.")
    if end_date <= start_date:
        raise ValidationError("End date must be after start date.")
    


class Vacation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank= False, null=False)
    description = models.TextField()
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    image = models.ImageField(upload_to='uploads/', blank=False, null=False)

    def clean(self):
        
        validate_date(self.start_date, self.end_date)
    class Meta:
        unique_together = ('country', 'start_date', 'end_date')


class Likes(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=False, null=False)
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE, related_name='likes', blank=False, null=False)

    class Meta:
        unique_together = ('user', 'vacation')

