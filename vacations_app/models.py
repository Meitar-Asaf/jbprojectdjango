from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date
# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        """
        Return the name of the country as a string
        This is used when representing the object in the admin interface
        or when printing the object
        """
        return self.country_name
    

    
    


class Vacation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank= False, null=False)
    description = models.TextField()
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def clean(self):
        """
        This method is called by Django's model validation system to
        perform any custom validation. It is called after the model's
        built-in validation has been performed.

        This method raises a ValidationError if any of the following
        conditions are not met:

        - start_date is in the future
        - end_date is after start_date
        - price is greater than 0
        - price is less than 10000
        - description is at least 10 characters long
        - image is not None
        """
        super().clean()
        if not self.pk:
            if self.start_date <= date.today():
                raise ValidationError("Start date must be in the future.")
            if self.image is None:
                raise ValidationError("Image is required.")
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")
        if self.price < 0:
            raise ValidationError("Price must be greater than 0")
        if self.price > 10000:
            raise ValidationError("Price must be less than 10000")
        if len(self.description) < 10:
            raise ValidationError("Description must be at least 10 characters long.")
            
    class Meta:
        unique_together = ('country', 'start_date', 'end_date')


class Likes(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,related_name='likes', blank=False, null=False)
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE, related_name='likes', blank=False, null=False)

    class Meta:
        unique_together = ('user', 'vacation')

