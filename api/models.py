from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=250)
    location = models.TextField()
    employee_size = models.IntegerField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    works_at = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='works_at')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
