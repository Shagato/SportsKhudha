from django.db import models
from datetime import datetime

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UpComingProducts(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/upcoming/')

    def __str__(self):
        return self.name