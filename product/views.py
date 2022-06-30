from .models import Product, Cart, WishList, Brand, Favourites, Review, Category, Order, Invoice
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from store.models import Customer
from django.urls import reverse_lazy
from django.db.models import Count

class AddCategory(CreateView):
    model = Category
    fields = ['name']
    template_name = 'product/add_category.html'
    success_url = reverse_lazy('grocery_store_home')


class ProductView(View):
    def get(self, request):
        return render(request, 'product/view_products.html', {'products':Product.objects.filter(brand=self.request.user.brand)})


class UpdateProductView(UpdateView):
    model = Product
    fields = ['name', 'price', 'image', 'description', 'available_quantity',  'discount', 'category', 'volume', 'volume_unit']
    template_name = 'product/update_product.html'
    success_url = reverse_lazy('grocery_store_home')



class AddProductView(CreateView):
    model = Product
    fields = ['name', 'price', 'image', 'description', 'available_quantity',  'discount', 'category', 'volume', 'volume_unit']
    template_name = 'product/add_product.html'
    success_url = reverse_lazy('grocery_store_home')


    def form_valid(self, form):
        form.instance.brand = Brand.objects.get(user=self.request.user)
        form.instance.no_of_purchases = 0
        return super(AddProductView, self).form_valid(form)



class UpdateBrandName(UpdateView):
    model = Brand
    fields = ['brand']
    template_name = 'product/update_brand_name.html'
    success_url = reverse_lazy('grocery_store_home')


class OnlyAddress(View):
    def get(self, request):
        return render(request, 'product/only_address.html', {})


class AddAddressOnlyView(View):
    def post(self, request):
        customer = Customer.objects.get(user=self.request.user)
        cart_products = Cart.objects.filter(customer=customer)
        address = self.request.POST.get('address-buy')
        total_amount = 0
        order = Order.objects.create(customer=customer, address=address, total_amount=0)
        for i in cart_products:
            product = i
            product.product.no_of_purchases += 1
            total_amount += product.product.calculate_discount * product.quantity
            Invoice.objects.create(order=order, product=product.product, quantity=product.quantity)
        Order.objects.filter(customer=customer, address=address, total_amount=0).update(total_amount=total_amount)
        Cart.objects.filter(customer=customer).delete()
        messages.success(request, "Order successful")
        return redirect('orders')


class AddAddressView(View):
    def post(self, request, pk):
        customer = Customer.objects.get(user=self.request.user)
        product = Product.objects.get(pk=pk)
        address = self.request.POST.get('address-buy')
        quantity = self.request.POST.get('quantityy')
        available_items = Product.objects.get(pk=pk).available_quantity
        if available_items >= float(quantity):
            items_left = available_items - float(quantity)
            order = Order.objects.create(customer=customer, address=address, total_amount=Product.objects.get(pk=pk).calculate_discount)
            Invoice.objects.create(order=order, product=product, quantity=quantity)
            number_purchased = Product.objects.get(pk=pk).no_of_purchases
            number_purchased += float(quantity)
            Product.objects.filter(pk=pk).update(no_of_purchases=number_purchased)
            Product.objects.filter(pk=pk).update(available_quantity=items_left)
            messages.success(request, "Order successful")
            return redirect('orders')
        else:
            messages.success(request, "Item not available in that quantity")
            return redirect('grocery_store_home')



class OrderDetailsView(View):
    def get(self, request, pk):
        return render(request, 'product/buy_address.html', {'pk':pk})


class PurchasedView(View):
    def get(self, request):
        orders = Order.objects.filter(customer=Customer.objects.get(user=self.request.user))
        items = []
        for i in orders:
            items += Invoice.objects.filter(order=i)

        return render(request, 'product/view_purchased.html', {'items':items})


class FilterProduct(View):
    def get(self, request):
        min_val = request.GET.get('min_val') if request.GET.get('min_val') != '' else \
        Product.objects.order_by('price').values_list('price', flat=True)[0]

        # values() --> Dictionary --> < QuerySet[{'comment_id': 1}, {'comment_id': 2}] >
        # values_list() --> Tuples --> < QuerySet[(1,), (2,)] >
        # values_list() with single field, flat=True --> single values instead of 1-tuples: --> < QuerySet[1, 2] >

        # gives all products in tuple
        # print(Product.objects.order_by('-price').values_list())

        # gives all product prices in list
        # print(Product.objects.order_by('-price').values_list('price', flat=True))

        # gives the 1st value
        # print(Product.objects.order_by('-price').values_list('price', flat=True)[0])

        max_val = request.GET.get('max_val') if request.GET.get('max_val') != '' else \
        Product.objects.order_by('-price').values_list('price', flat=True)[0]
        products = Product.objects.filter(price__gte=float(min_val), price__lte=float(max_val))
        return render(request, 'product/filter_result.html', {'products': products})


class CategoryView(ListView):
    def get(self, request, category):
        # category = self.request.POST.get('category')
        products = Product.objects.filter(category=Category.objects.get(name=category))
        return render(request, 'product/filter_result.html', {'products': products, 'category': Category.objects.all()})


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
            return render(request, 'product/favourites.html',
                          {'products': products, 'all_brands': all_brands, 'fav': fav})
        else:
            messages.error(request, "You have no favourites")
            return render(request, 'product/favourites.html', {'all_brands': all_brands, })


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


# class HomeView(ListView):
#     template_name = 'product/home.html'
#     model = Product
#     context_object_name = 'products'
#     # 'purchases': Product.objects.order_by('-no_of_purchases')[0:5]
#     # 'reviews' : Review.objects.order_by('-product')[0:5]
#     # 'wishlist' : WishList.objects.order_by('-product')[0:5]
#
#     extra_context = {
#         'category': Category.objects.all(),
#         'trendings': Product.objects.order_by('-no_of_purchases')[0:5]
#     }

class HomeView(View):
    def get(self, request):
        if request.user.is_staff:
            brand = Brand.objects.get(user=request.user)
            return render(request,'product/admin_func.html', {'brand':brand})
        elif request.user.is_superuser:
            return redirect('admin:index')
        else:
            products = Product.objects.all()
            category = Category.objects.all()

            trendings = Product.objects.order_by('-no_of_purchases').distinct()[0:5]
            all_products = trendings

            review_id = Review.objects.values_list('product').annotate(product_count=Count('product')).order_by(
                '-product_count')[0:5]
            # <QuerySet [(20, 3), (21, 1), (23, 1), (22, 1)]>
            for i in review_id:
                all_products |= Product.objects.filter(pk=i[0])

            wishlist_id = WishList.objects.values_list('product').annotate(product_count=Count('product')).order_by(
                '-product_count')[0:5]
            for i in wishlist_id:
                all_products |= Product.objects.filter(pk=i[0])

            return render(request, 'product/home.html',
                          {'products': products, 'category': category, 'all_products': all_products})


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
