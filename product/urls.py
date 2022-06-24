from django.urls import path
from .views import DetailProductView, SearchProduct, CartView, AddToCart, WishListView, AddToWishList, \
    RemoveFromWishList, RemoveFromCart, UpdateCart, AddToFavourites, FavouriteView, RemoveFromFavourites, \
    AddReviewView, CategoryView, FilterProduct

urlpatterns = [
    path('search/', SearchProduct.as_view(), name='product-search'),
    path('<int:pk>/', DetailProductView.as_view(), name='product-detail'),

    path('<int:pk>/add_to_cart/', AddToCart.as_view(), name="add-to-cart"),
    path('cart/', CartView.as_view(), name='cart'),
    path('<int:pk>/remove_from_cart/', RemoveFromCart.as_view(), name="remove-from-cart"),
    path('cart/<int:pk>/', UpdateCart.as_view(), name="update-cart"),

    path('<int:pk>/add_to_wishlist/', AddToWishList.as_view(), name="add-to-wishlist"),
    path('<int:pk>/remove_from_wishlist/', RemoveFromWishList.as_view(), name="remove-from-wishlist"),
    path('wishlist/', WishListView.as_view(), name='wishlist'),

    path('favourites/', FavouriteView.as_view(), name='favourites'),
    path('<int:pk>/add_to_favourites/', AddToFavourites.as_view(), name='add-to-favourites'),
    path('<int:pk>/remove_from_favourites/', RemoveFromFavourites.as_view(), name='remove-from-favourites'),

    path('<int:pk>/review/', AddReviewView.as_view(), name='add-review'),

    path('category/<str:category>/', CategoryView.as_view(), name='view-category'),
    path('filter/', FilterProduct.as_view(), name='price-filter'),
]
