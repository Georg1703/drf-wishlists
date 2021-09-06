from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)

from ..models import Product, WishList, WishListProduct
from .serializers import ProductSerializer, WishListSerializer, WishListProductSerializer


class ProductViewSet(CreateModelMixin,
                     ListModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]


class WishListViewSet(CreateModelMixin,
                      ListModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = WishListSerializer
    queryset = WishList.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def list(self, request, *args, **kwargs):
        queryset = WishList.objects.filter(user=request.user)
        serializer = WishListSerializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=True)
    def add_to_wishlist(self, request):
        serializer = WishListProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True)
    def delete_product_from_wishlist(self, request, *args, **kwargs):
        serializer = WishListProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.delete()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True)
    def list_products_from_wishlist(self, request, *args, **kwargs):
        data = {}
        wishlist_id = int(str(request).split('/')[-2])

        if WishList.objects.filter(id=wishlist_id, user=request.user).exists():
            wishlist = WishList.objects.get(id=wishlist_id)
            products = wishlist.wishlistproduct_set.all()
            data['products'] = [elem.product.name for elem in products]
        else:
            data['wishlist'] = 'does not exist'

        return Response(data)


