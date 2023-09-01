from django.db import models

# Create your models here.

class DemoModel02(models.Model):
    choices = [
        ('manager', "Manager"),
        ('trainee', "Trainee"),
        ('intern', "Intern")
    ]
    name = models.CharField(max_length=200, default=None, blank=True)
    salary = models.BigIntegerField(null=True,default=None)
    age = models.IntegerField(default=18, null=True)
    designation = models.CharField(default="manager",max_length=20, choices=choices)