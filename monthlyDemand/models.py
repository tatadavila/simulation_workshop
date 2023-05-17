from django.db import models


# Create your models here.
class Product(models.Model):
    nombre = models.CharField(max_length=100)


class MonthlyDemand(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    demand = models.IntegerField()
    fecdateha = models.DateField(auto_now_add=True)
