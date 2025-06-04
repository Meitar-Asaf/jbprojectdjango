from django.db import models

# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return self.country_name

class Vacation(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='vacation_images/')


class Likes(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'vacation')

