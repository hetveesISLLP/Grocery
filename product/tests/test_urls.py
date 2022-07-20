# from django.urls import reverse, resolve
# from product.views import DetailProductView, SearchProduct, CartView, AddToCart, WishListView, AddToWishList, \
#     RemoveFromWishList, RemoveFromCart, UpdateCart, AddToFavourites, FavouriteView, RemoveFromFavourites, \
#     AddReviewView, CategoryView, FilterProduct, OrderDetailsView, PurchasedView, OnlyAddress, \
#     AddCategory, UpdateBrandName, AddProductView, ProductView, UpdateProductView, \
#     DetailPurchasedView, DownloadInvoice, ViewOrdersVendor, UpdateOrderStatus, \
#     ViewCheckout, FailureView, CreateCheckoutSession, PaymentSuccessView, CreateCheckoutSessionCart, \
#     PaymentSuccessViewCart, ReturnProductView, ReturnStatus
#
# from django.contrib.auth import views as auth_views
# from django.test import TestCase
#
#
# class TestUrls(TestCase):
#
#     pk=1
#     category='Flour'
#
#     def test_search_url(self):
#         url = reverse('product-search')
#         self.assertEqual(resolve(url). func.view_class, SearchProduct)
#
#     def test_cart_url(self):
#         url = reverse('cart')
#         self.assertEqual(resolve(url). func.view_class, CartView)
#
#     def test_wishlist_url(self):
#         url = reverse('wishlist')
#         self.assertEqual(resolve(url). func.view_class, WishListView)
#
#     def test_favourites_url(self):
#         url = reverse('favourites')
#         self.assertEqual(resolve(url). func.view_class, FavouriteView)
#
#     def test_price_filter_url(self):
#         url = reverse('price-filter')
#         self.assertEqual(resolve(url). func.view_class, FilterProduct)
#
#     def test_orders_url(self):
#         url = reverse('orders')
#         self.assertEqual(resolve(url). func.view_class, PurchasedView)
#
#     def test_add_category_url(self):
#         url = reverse('add-category')
#         self.assertEqual(resolve(url). func.view_class, AddCategory)
#
#     def test_view_product_url(self):
#         url = reverse('view-product')
#         self.assertEqual(resolve(url). func.view_class, ProductView)
#
#     def test_product_detail_url(self):
#         url = reverse('product-detail', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, DetailProductView)
#
#     def test_add_to_cart_url(self):
#         url = reverse('add-to-cart', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, AddToCart)
#
#     def test_remove_from_cart_url(self):
#         url = reverse('remove-from-cart', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, RemoveFromCart)
#
#     def test_update_cart_url(self):
#         url = reverse('update-cart', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, UpdateCart)
#
#     def test_add_to_wishlist_url(self):
#         url = reverse('add-to-wishlist', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, AddToWishList)
#
#     def test_remove_from_wishlist_url(self):
#         url = reverse('remove-from-wishlist', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, RemoveFromWishList)
#
#     def test_add_to_favourites_wishlist_url(self):
#         url = reverse('add-to-favourites', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, AddToFavourites)
#
#     def test_detail_orders_url(self):
#         url = reverse('detail-orders', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, DetailPurchasedView)
#
#     def test_remove_from_favourites_url(self):
#         url = reverse('remove-from-favourites', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, RemoveFromFavourites)
#
#     def test_add_review_url(self):
#         url = reverse('add-review', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, AddReviewView)
#
#     def test_view_category_url(self):
#         url = reverse('view-category', kwargs={'category':self.category})
#         self.assertEqual(resolve(url). func.view_class, CategoryView)
#
#     def test_update_brand_name_url(self):
#         url = reverse('update-brand_name', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, UpdateBrandName)
#
#     def test_add_product_url(self):
#         url = reverse('add-product', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, AddProductView)
#
#     def test_update_product_url(self):
#         url = reverse('update-product', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, UpdateProductView)
#
#     def test_download_invoice_url(self):
#         url = reverse('download-invoice', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, DownloadInvoice)
#
#     def test_view_order_url(self):
#         url = reverse('view-order')
#         self.assertEqual(resolve(url). func.view_class, ViewOrdersVendor)
#
#     def test_update_product_status_url(self):
#         url = reverse('update-product-status', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, UpdateOrderStatus)
#
#     def test_create_session_url(self):
#         url = reverse('create-session')
#         self.assertEqual(resolve(url). func.view_class, CreateCheckoutSession)
#
#     def test_view_checkout_url(self):
#         url = reverse('view-checkout')
#         self.assertEqual(resolve(url). func.view_class, ViewCheckout)
#
#     def test_return_product_url(self):
#         url = reverse('return-product', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, ReturnProductView)
#
#     def test_return_status_url(self):
#         url = reverse('return-status', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url). func.view_class, ReturnStatus)
#
#     def test_buy_now_url(self):
#         url = reverse('buy-now', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url).func.view_class, OrderDetailsView)
#
#     def test_buy_now_cart_url(self):
#         url = reverse('buy-now-cart')
#         self.assertEqual(resolve(url).func.view_class, OnlyAddress)
#
#     def test_checkout_address_url(self):
#         url = reverse('checkout-address')
#         self.assertEqual(resolve(url).func.view_class, CreateCheckoutSessionCart)
#
#     def test_api_checkout_session_url(self):
#         url = reverse('api_checkout_session', kwargs={'pk':self.pk})
#         self.assertEqual(resolve(url).func.view_class, CreateCheckoutSession)
#
#     def test_success_url(self):
#         url = reverse('success')
#         self.assertEqual(resolve(url).func.view_class, PaymentSuccessView)
#
#     def test_success_cart_url(self):
#         url = reverse('success-cart')
#         self.assertEqual(resolve(url). func.view_class, PaymentSuccessViewCart)
#
#     def test_failure_url(self):
#         url = reverse('failure')
#         self.assertEqual(resolve(url). func.view_class, FailureView)
#
