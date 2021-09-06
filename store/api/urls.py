from django.urls import path
from .views import ProductViewSet, WishListViewSet
from rest_framework.urlpatterns import format_suffix_patterns

product_list = ProductViewSet.as_view({
   'get': 'list',
   'post': 'create',
})

product_detail = ProductViewSet.as_view({
   'delete': 'destroy',
   'put': 'update',
})

wishlist_list = WishListViewSet.as_view({
   'get': 'list',
   'post': 'create',
})

wishlist_detail = WishListViewSet.as_view({
   'delete': 'destroy',
   'put': 'update',
   'get': 'list_products_from_wishlist',
})

wishlist_add_product = WishListViewSet.as_view({
   'post': 'add_to_wishlist',
   'delete': 'delete_product_from_wishlist'
})

urlpatterns = format_suffix_patterns([
   path('products/', product_list, name='product-list'),
   path('product/<int:pk>/', product_detail, name='product-detail'),

   path('wishlists/', wishlist_list, name='wishlist_list'),
   path('wishlist/<int:pk>/', wishlist_detail, name='wishlist_detail'),

   path('wishlist/product/', wishlist_add_product, name='wishlist_add_product'),
])