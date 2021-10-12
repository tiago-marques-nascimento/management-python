from datetime import date
from django.db import models
from .base_entity_viewmodel import BaseEntityViewModel

class StoreViewModel(BaseEntityViewModel):
    def __init__(self, store = None):
        self.id = None if store == None else store.id
        self.name = "" if store == None else store.name
        self.launched_at = date.today() if store == None else store.launched_at
        self.products = [] if store == None else map(lambda storeProduct: ProductViewModel(storeProduct.product), store.storeproduct_set.all())

class ProductViewModel(BaseEntityViewModel):
    def __init__(self, product = None):
        self.id = None if product == None else product.id
        self.name = "" if product == None else product.name
        self.description = "" if product == None else product.description
