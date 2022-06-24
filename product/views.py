from .models import Product, Cart, WishList, Brand, Favourites, Review
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.views.generic.base import View
from store.models import Customer


class AddReviewView(View):
    def post(self, request, pk):
        customer = Customer.objects.get(user=request.user)
        review = self.request.POST.get('add_review')
        product = Product.objects.get(pk=pk)
        Review.objects.create(customer=customer, review=review, product=product)
        messages.success(request, "Review added successfully")
        return redirect('product-detail', pk=pk)


class FavouriteView(View):
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        fav = Favourites.objects.filter(customer=customer.id)

        all_brands = Brand.objects.all()

        if len(fav) >= 1:
            products = Product.objects.filter(brand=fav[0].brand)
            for item in fav[1:]:
                products |= Product.objects.filter(brand=item.brand)
            return render(request, 'product/favourites.html', {'products':products, 'all_brands':all_brands, 'fav':fav})
        else:
            messages.error(request, "You have no favourites")
            return render(request, 'product/favourites.html', {'all_brands':all_brands,})


class RemoveFromFavourites(View):
    def get(self, request, pk):
        brand = Brand.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        Favourites.objects.filter(customer=customer, brand=brand).delete()
        messages.success(request, "Brand removed from Favourites.")
        return redirect('favourites')


class AddToFavourites(View):
    def get(self, request, pk):
        brand = Brand.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        try:
            Favourites.objects.get(customer=customer, brand=brand)
            messages.error(request, 'Brand Already exist in Favourites')
            return redirect('favourites')
        except:
            Favourites.objects.create(customer=customer, brand=brand)
            messages.success(request, "Brand added to Favourites.")
            return redirect('favourites')


class RemoveFromWishList(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        WishList.objects.filter(customer=customer, product=product).delete()
        messages.success(request, "Item removed from WishList.")
        return redirect('wishlist')


class RemoveFromCart(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        Cart.objects.filter(customer=customer, product=product).delete()
        messages.success(request, "Item removed from Cart.")
        return redirect('cart')


class AddToWishList(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        try:
            WishList.objects.get(customer=customer, product=product)
            messages.error(request, 'Item Already exist')
            return redirect('wishlist')
        except:
            WishList.objects.create(customer=customer, product=product)
            messages.success(request, "Item added to WishList.")
            return redirect('wishlist')


class WishListView(ListView):
    template_name = 'product/wishlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = WishList.objects.filter(customer=Customer.objects.get(user=self.request.user))
        return products


class AddToCart(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        quantity = 1
        try:
            Cart.objects.get(customer=customer, product=product)
            messages.error(request, 'Item Already exist in cart')
            return redirect('cart')
        except:
            Cart.objects.create(customer=customer, product=product, quantity=quantity)
            messages.success(request, "Item added to Cart.")
            return redirect('cart')


class UpdateCart(View):
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer, product=product)
        cart.quantity = self.request.POST.get('quantity')
        cart.save()
        return redirect('cart')


class CartView(ListView):
    template_name = 'product/add_to_cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Cart.objects.filter(customer=Customer.objects.get(user=self.request.user))
        return products


class HomeView(ListView):
    template_name = 'product/home.html'
    model = Product
    context_object_name = 'products'


class DetailProductView(DetailView):
    model = Product


class SearchProduct(View):
    def post(self, request):
        searched = request.POST['searched']
        products_name = Product.objects.filter(
            Q(name__icontains=searched) |
            Q(description__icontains=searched) |
            Q(brand__brand__icontains=searched) |
            Q(category__name__icontains=searched)).distinct()

        return render(request,
                      'product/search.html',
                      {
                          'searched': searched,
                          'products_name': products_name,
                      }
                      )
