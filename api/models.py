from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=250)
    location = models.TextField()
    employee_size = models.IntegerField()
