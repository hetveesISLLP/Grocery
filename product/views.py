from .models import Product, Cart, WishList
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from store.models import Customer
from django.contrib.auth.mixins import LoginRequiredMixin




class AddToWishList(View):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        WishList.objects.create(customer=customer, product=product)
        messages.success(request, "Item added to WishList.")
        return redirect('wishlist')


class WishListView(ListView):
    template_name = 'product/wishlist.html'
    # model = Cart
    context_object_name = 'products'

    def get_queryset(self):
        products = WishList.objects.filter(customer=Customer.objects.get(user=self.request.user))
        return products


class AddToCart(View):

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        quantity = 1
        # cart = Cart.objects.create(customer=customer, product=product, quantity=quantity)
        Cart.objects.create(customer=customer, product=product, quantity=quantity)
        messages.success(request, "Item added to cart")
        return redirect('cart')
        # return render(request, 'product/add_to_cart.html', {'cart':cart})

    # def get_queryset(self, request):
    #     product = Product.objects.get(pk=pk)
    #     customer = Customer.objects.get(user=request.user)
    #     quantity = 1
    #     # cart = Cart.objects.create(customer=customer, product=product, quantity=quantity)
    #     Cart.objects.create(customer=customer, product=product, quantity=quantity)
    #     messages.success(request, "Item added")
    #     return redirect('cart')
    #     # return render(request, 'product/add_to_cart.html', {'cart':cart})



# def addtocart(request, pk):
#     product = Product.objects.get(pk=pk)
#     customer = Customer.objects.get(user=request.user)
#     Cart.objects.create(customer=customer, product=product, quantity=1)
#     messages.success(request, "Item added")
#     return redirect('cart')


class CartView(ListView):
    template_name = 'product/add_to_cart.html'
    # model = Cart
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


