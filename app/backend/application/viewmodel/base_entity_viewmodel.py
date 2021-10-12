import uuid
from django.db import models

class BaseEntityViewModel():
    def __init__(self, id):
        pass

    class Meta:
        abstract = True
