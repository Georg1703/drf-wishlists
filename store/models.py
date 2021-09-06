from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers
import uuid


def get_uuid_code(length: int = 8) -> str:
    return str(uuid.uuid4())[:length].upper()


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=8, default=get_uuid_code, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name


class WishList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WishListProduct(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['wishlist', 'product']

    def __str__(self):
        return f'{self.wishlist.name} {self.product.name}'
