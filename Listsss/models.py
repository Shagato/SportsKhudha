# MyApp/models.py

from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='item_images/', null=True, blank=True)

    def __str__(self):
        return self.name
