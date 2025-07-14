from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
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
    description = models.TextField(blank=False, null=False, validators=[MinLengthValidator(10, message="Description must be at least 10 characters")])
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    image = models.ImageField(upload_to='vacation_images/', blank=True, null=True)

    def clean(self):
       
       
        """
        This method is called after the model's built-in validation is done, and
        is used to add additional validation to the model.

        The method raises a ValidationError if the start date is in the past,
        if there is no image, if the end date is before the start date, if the
        price is not greater than 0 or less than 10000, or if the description
        is less than 10 characters long.

        The method calls the parent class's clean method first, to ensure that
        the model's built-in validation is done first.

        The method is called when the model instance is saved, and is used to
        validate the entire model instance before it is saved to the database.
        """
       
        super().clean()

        if not self.pk:
            if self.start_date and self.start_date <= date.today():
                raise ValidationError("Start date must be in the future.")
            if not self.image:
                raise ValidationError("Image is required.")

        if not self.country_id:
            raise ValidationError("Country is required.")

        if not Country.objects.filter(pk=self.country_id).exists():
            raise ValidationError("Country does not exist.")

        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

        if self.price is not None:
            if self.price < 0:
                raise ValidationError("Price must be greater than 0")
            if self.price > 10000:
                raise ValidationError("Price must be less than 10000")

        if self.description and len(self.description) < 10:
            raise ValidationError("Description must be at least 10 characters long.")

        
        
    def save(self, *args, **kwargs):
        
        """
        Override the default save method to call full_clean before saving.

        The full_clean method is called to validate the entire model instance
        before it is saved to the database. This is necessary because the
        model's built-in validation is not enough to validate the entire
        instance, and we need to call the clean method to add additional
        validation.

        The parent class's save method is called after full_clean to save the
        instance to the database.

        This method is called when the model instance is saved.
        """
        
        self.full_clean()
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        """
        Override the default delete method to delete the image as well.

        The image.delete() method is called with save=False to prevent the
        image from being saved after deletion. This is necessary because the
        image is being deleted by the model's delete method, and we don't want
        the image to be saved after deletion.

        This method is called when the model instance is deleted. It deletes the
        image associated with the instance, and then calls the parent class's
        delete method to delete the instance itself.
        """

        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
            
    class Meta:
        unique_together = ('country', 'start_date', 'end_date')
        ordering = ['start_date']


class Likes(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,related_name='likes', blank=False, null=False)
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE, related_name='likes', blank=False, null=False)

    class Meta:
        unique_together = ('user', 'vacation')

