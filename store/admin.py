from django.contrib import admin
from .models import Product, WishList, WishListProduct

admin.site.register(Product)
admin.site.register(WishList)
admin.site.register(WishListProduct)
