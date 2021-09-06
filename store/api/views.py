from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)

from ..models import Product, WishList, WishListProduct
from .serializers import ProductSerializer, WishListSerializer


class ProductViewSet(CreateModelMixin,
                     ListModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class WishListViewSet(CreateModelMixin,
                      ListModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = WishListSerializer
    queryset = WishList.objects.all()

    @action(detail=False)
    def list(self, request, *args, **kwargs):
        queryset = WishList.objects.filter(user=request.user)
        serializer = WishListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def add_to_wishlist(self, request, *args, **kwargs):
        data = {
            'response': 'product was added to wishlist'
        }
        wishlist_id = request.data['wishlist']
        product_id = request.data['product']
        product = wishlist = ''

        if not WishList.objects.filter(id=wishlist_id, user=request.user).exists():
            data['response'] = 'wishlist does not exist'
        wishlist = WishList.objects.get(id=wishlist_id, user=request.user)

        if not Product.objects.filter(id=product_id).exists():
            data['response'] = 'product does not exist'
        product = Product.objects.get(id=product_id)

        try:
            relation = WishListProduct(wishlist=wishlist, product=product)
            relation.save()
            return Response(data)
        except:
            return Response(data)


    @action(detail=True)
    def delete_product_from_wishlist(self, request, *args, **kwargs):
        pass


    @action(detail=True)
    def list_products_from_wishlist(self, request, *args, **kwargs):
        data = {}
        wishlist_id = int(str(request).split('/')[-2])

        if WishList.objects.filter(id=wishlist_id, user=request.user).exists():
            wishlist = WishList.objects.get(id=wishlist_id)
            products = wishlist.wishlistproduct_set.all()
            data['products'] = [elem.product.name for elem in products]
        else:
            data['response'] = 'wishlist does not exist'

        return Response(data)


