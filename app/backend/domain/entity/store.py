from django.db import models
from .base_entity import BaseEntity

class Store(BaseEntity):
    name = models.CharField(max_length=100, unique=True)
    launched_at = models.DateTimeField()

class Product(BaseEntity):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)

class StoreProduct(BaseEntity):
    store = models.ForeignKey(Store, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
