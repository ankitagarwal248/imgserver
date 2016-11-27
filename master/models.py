from __future__ import unicode_literals

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=1000, blank=True, null=True)
    image256 = models.CharField(max_length=1000, blank=True, null=True)
    image512 = models.CharField(max_length=1000, blank=True, null=True)

