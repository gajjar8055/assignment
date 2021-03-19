from django.db import models


# Create your models here.
class MovieDetails(models.Model):
    name = models.CharField(max_length=300, null=True)
    ratings = models.DecimalField(max_digits=2, decimal_places=1)
    release_date = models.DateField()
    duration = models.TimeField()
    description = models.TextField()
