from rest_framework import serializers
from ..models import Product, WishList, WishListProduct


class ProductSerializer(serializers.ModelSerializer):
    appears_in_wishlists = serializers.SerializerMethodField('count_appears_in_wishlist')

    class Meta:
        model = Product
        fields = '__all__'

    def count_appears_in_wishlist(self, obj):
        return obj.wishlistproduct_set.all().count()


class WishListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WishList
        fields = ['id', 'name', 'user']


class WishListProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = WishListProduct
        fields = ['wishlist', 'product']