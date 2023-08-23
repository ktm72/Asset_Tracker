from django.db import models
from datetime import date
from rest_framework.response import Response


class Company(models.Model):
    name = models.CharField(max_length=250)
    location = models.TextField()
    employee_size = models.IntegerField()

    def __str__(self) -> str:
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
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.first_name + self.last_name


class Gear(models.Model):
    owner = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=150)
    gear_type = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class GearLog(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='company')
    device = models.ForeignKey(
        Gear, on_delete=models.SET_NULL, related_name='device', null=True)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, related_name='employee', null=True)
    period = models.IntegerField(default=5)
    returned = models.BooleanField(default=False)
    condition = models.TextField()
    returned_condition = models.TextField(null=True, blank=True)
    checkout_date = models.DateField(default=date.today)
    returned_date = models.DateField(null=True, blank=True)
