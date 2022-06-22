from django.urls import path
from .views import DetailProductView, SearchProduct, CartView, AddToCart, WishListView, AddToWishList, \
    RemoveFromWishList, RemoveFromCart, UpdateCart

urlpatterns = [
    path('search/', SearchProduct.as_view(), name='product-search'),
    path('<int:pk>/', DetailProductView.as_view(), name='product-detail'),
    path('<int:pk>/add_to_cart/', AddToCart.as_view(), name="add-to-cart"),
    path('cart/', CartView.as_view(), name='cart'),
    path('<int:pk>/add_to_wishlist/', AddToWishList.as_view(), name="add-to-wishlist"),
    path('<int:pk>/remove_from_wishlist/', RemoveFromWishList.as_view(), name="remove-from-wishlist"),
    path('<int:pk>/remove_from_cart/', RemoveFromCart.as_view(), name="remove-from-cart"),
    path('cart/<int:pk>/', UpdateCart.as_view(), name="update-cart"),
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    ]
