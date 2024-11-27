from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', ProductDetailUpdateDeleteView.as_view(), name='product_detail_update_delete'),
    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', CategoryDetailUpdateDeleteView.as_view(), name='category_update'),  # فقط سوپر یوزر
    path('categories/<int:pk>/products/', CategoryProductsView.as_view(), name='category_products'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/', ViewCartView.as_view(), name='view_cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
]
