from .models import Product, Cart, WishList, Brand, Favourites, Review, Category, Order, Invoice
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from store.models import Customer
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseNotFound
from django.db.models import Count
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import math

stripe.api_key = 'sk_test_51LGcerSBrStSbNNxHd8IMfYJULu1SZ0QhBJViYUcKPOPRo7qr12w9wOH93rqhy00OZHd0P321jijOOOr4sMqhWq000VDho2bON'


class FailureView(TemplateView):
    template_name = 'product/failure_payment.html'


class ViewCheckout(TemplateView):
    template_name = 'product/view_checkout.html'


class PaymentSuccessViewCart(View):
    template_name = "product/success_payment.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        customer = Customer.objects.get(user=request.user)
        total_amount = 0
        order = get_object_or_404(Order, stripe_payment_intent=session.payment_intent)

        invoices = []
        cart_products = Cart.objects.filter(customer=customer)

        for i in cart_products:
            product = i
            i.product.available_quantity -= i.quantity
            i.product.save()
            total_amount += int(float(product.product.calculate_discount) * product.quantity)
            invoices.append(Invoice(product=product.product, quantity=product.quantity))

        order.has_paid = True
        order.address = request.GET.get('address')
        order.total_amount = total_amount
        order.save()
        Cart.objects.filter(customer=customer).delete()

        for i in invoices:
            i.order = order
            i.save()

        return render(request, self.template_name)


class CreateCheckoutSessionCart(View):
    @method_decorator(csrf_exempt)
    def post(self, request):
        customer = Customer.objects.get(user=self.request.user)
        cart_products = Cart.objects.filter(customer=customer)

        detail = request.body.decode('utf-8')
        body = json.loads(detail)
        address = body['address-buy']

        '''for checking the quantity'''
        for i in cart_products:
            if i.product.available_quantity >= i.quantity:
                pass
            else:
                messages.error(request, "Item not available in that quantity")
                return JsonResponse({'message': False})
        else:
            lis = []
            for cproduct in cart_products:
                lis.append({
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(float(cproduct.product.calculate_discount)*100),
                        'product_data':
                            {
                                'name': cproduct.product.name
                            },
                    },
                    'quantity': cproduct.quantity
                })

            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=lis,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success-cart')) + "?session_id={CHECKOUT_SESSION_ID}&address="+address,
                cancel_url=request.build_absolute_uri(reverse('failure')),
            )

            Order.objects.create(customer=customer, total_amount=0, stripe_payment_intent=session['payment_intent'])

            return JsonResponse({'sessionId': session.id})


class PaymentSuccessView(View):
    template_name = "product/success_payment.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        prod_pk = int(request.GET.get('product'))
        product = Product.objects.get(pk=prod_pk)
        address = request.GET.get('address')
        quantity = int(request.GET.get('quantity'))

        order = get_object_or_404(Order, stripe_payment_intent=session.payment_intent)
        order.total_amount = float(product.calculate_discount) * int(quantity)
        order.address = address
        order.has_paid = True
        order.save()

        invoice = Invoice()
        invoice.order = order
        invoice.product = product
        invoice.quantity = quantity
        invoice.save()

        product.available_quantity -= quantity
        product.no_of_purchases += quantity
        product.save()

        return render(request, self.template_name)


''' This view serves as an API to initialize the payment gateway.'''


class CreateCheckoutSession(View):
    @method_decorator(csrf_exempt)
    def post(self, request, pk):
        customer = Customer.objects.get(user=self.request.user)
        product = Product.objects.get(pk=pk)

        detail = request.body.decode('utf-8')
        body = json.loads(detail)

        available_items = Product.objects.get(pk=pk).available_quantity
        number_purchased = Product.objects.get(pk=pk).no_of_purchases
        address = body['address-buy']
        quantity = body['quantityy']
        '''for checking the quantity'''
        if available_items >= float(quantity):
            items_left = available_items - float(quantity)
            number_purchased += float(quantity)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(float(product.calculate_discount) * 100),
                        'product_data': {
                            'name': product.name
                        },
                    },
                    'quantity': quantity
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')) + "?session_id={CHECKOUT_SESSION_ID}&address="+address+"&quantity="+str(quantity)+"&product="+str(pk),
                cancel_url=request.build_absolute_uri(reverse('failure')),

            )

            Order.objects.create(customer=customer, stripe_payment_intent=session['payment_intent'], total_amount=0)



            return JsonResponse({'sessionId': session.id})
        else:
            messages.error(request, "Item not available in that quantity")
            return JsonResponse({'message': False})


'''For updating the status of the products'''


class UpdateOrderStatus(UpdateView):
    model = Invoice
    fields = ['status']
    template_name = 'product/update_order_status.html'
    success_url = reverse_lazy('view-order')


'''For viewing the orders of the brand of the vendor'''


class ViewOrdersVendor(View):
    def get(self, request):
        invoice = Invoice.objects.filter(product__brand=self.request.user.brand)
        return render(request, 'product/view_order_vendor.html', {'invoice': invoice})


class DownloadInvoice(View):
    def get(self, request, pk):
        # template = get_template('product/detail_order.html')
        order = Order.objects.get(pk=pk)
        invoice = Invoice.objects.filter(order=order)
        context = {

            'all_orders': Invoice.objects.filter(order=pk),
            'order': order,
            'order_ids': order.id
        }
        pdf = RenderToPdf('product/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % context['order_ids']

            content = "file; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def RenderToPdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


'''For adding the category'''


class AddCategory(CreateView):
    model = Category
    fields = ['name']
    template_name = 'product/add_category.html'
    success_url = reverse_lazy('grocery_store_home')
    category = Category.objects.all()
    extra_context = {
        'category': category
    }


class ProductView(View):
    def get(self, request):
        return render(request, 'product/admin_func.html',
                      {'products': Product.objects.filter(brand=self.request.user.brand)})


# class DeleteProductView(DeleteView):
#     model = Product
#     template_name = 'product/delete_product.html'
#     success_url = reverse_lazy('grocery_store_home')


'''For updating the product'''


class UpdateProductView(UpdateView):
    model = Product
    fields = ['name', 'price', 'image', 'description', 'available_quantity', 'discount', 'category', 'volume',
              'volume_unit']
    template_name = 'product/update_product.html'
    success_url = reverse_lazy('view-product')


'''For adding the product'''


class AddProductView(CreateView):
    model = Product
    fields = ['name', 'price', 'image', 'description', 'available_quantity', 'discount', 'category', 'volume',
              'volume_unit']
    template_name = 'product/add_product.html'
    success_url = reverse_lazy('view-product')

    '''for setting the brand of product'''

    def form_valid(self, form):
        form.instance.brand = Brand.objects.get(user=self.request.user)
        form.instance.no_of_purchases = 0
        return super(AddProductView, self).form_valid(form)


'''For updating the brand name'''


class UpdateBrandName(UpdateView):
    model = Brand
    fields = ['brand']
    template_name = 'product/update_brand_name.html'
    success_url = reverse_lazy('view-product')


class OnlyAddress(View):
    def get(self, request):
        return render(request, 'product/only_address.html', {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})




'''For getting the address, quantity for order from the cart'''


class AddAddressOnlyView(View):
    def post(self, request):
        customer = Customer.objects.get(user=self.request.user)
        cart_products = Cart.objects.filter(customer=customer)
        address = self.request.POST.get('address-buy')
        total_amount = 0
        invoices = []

        '''for checking the quantity'''
        for i in cart_products:
            if i.product.available_quantity >= i.quantity:
                product = i
                i.product.available_quantity -= i.quantity
                i.product.save()
                total_amount += float(product.product.calculate_discount) * product.quantity
                invoices.append(Invoice(product=product.product, quantity=product.quantity))
            else:
                break
        else:
            order = Order.objects.create(customer=customer, address=address, total_amount=0)
            for i in invoices:
                i.order = order
                i.save()
            Order.objects.filter(customer=customer, address=address, total_amount=0).update(total_amount=total_amount)
            Cart.objects.filter(customer=customer).delete()
            messages.success(request, "Order successful")
            return redirect('orders')
        return redirect('grocery_store_home')


'''For getting the address, quantity for the single item order'''


class AddAddressView(View):
    def post(self, request, pk):
        customer = Customer.objects.get(user=self.request.user)
        product = Product.objects.get(pk=pk)
        address = self.request.POST.get('address-buy')
        quantity = self.request.POST.get('quantityy')
        available_items = Product.objects.get(pk=pk).available_quantity

        '''for checking the quantity'''
        if available_items >= float(quantity):
            items_left = available_items - float(quantity)
            order = Order.objects.create(customer=customer, address=address,
                                         total_amount=Product.objects.get(pk=pk).calculate_discount)
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
        return render(request, 'product/buy_address.html',
                      {'pk': pk, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


'''For viewing the order details'''


class PurchasedView(View):
    def get(self, request):
        items = Order.objects.filter(customer=Customer.objects.get(user=self.request.user))
        # items = []
        # for i in orders:
        #     items += Invoice.objects.filter(order=i)

        return render(request, 'product/view_purchased.html', {'items': items})


'''For viewing the details of the purchased products'''


class DetailPurchasedView(View):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        all_orders = Invoice.objects.filter(order=pk)
        return render(request, 'product/detail_order.html', {'all_orders': all_orders, 'order': order})


'''For filtering the product based on min and max price'''


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


'''For viewing products of the specified category'''


class CategoryView(ListView):
    def get(self, request, category):
        # category = self.request.POST.get('category')
        products = Product.objects.filter(category=Category.objects.get(name=category))
        return render(request, 'product/filter_result.html', {'products': products, 'category': Category.objects.all()})


'''For adding the review to the product'''


class AddReviewView(View):
    def post(self, request, pk):
        customer = Customer.objects.get(user=request.user)
        review = self.request.POST.get('add_review')
        product = Product.objects.get(pk=pk)
        Review.objects.create(customer=customer, review=review, product=product)
        messages.success(request, "Review added successfully")
        return redirect('product-detail', pk=pk)


'''For viewing all the products of the favourite brand'''


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


'''For removing brand from the favourites'''


class RemoveFromFavourites(View):
    def get(self, request, pk):
        brand = Brand.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        Favourites.objects.filter(customer=customer, brand=brand).delete()
        messages.success(request, "Brand removed from Favourites.")
        return redirect('favourites')


'''For adding brand to the Favourites if not already exists'''


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


'''For removing product from the Wishlist'''


class RemoveFromWishList(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        WishList.objects.filter(customer=customer, product=product).delete()
        messages.success(request, "Item removed from WishList.")
        return redirect('wishlist')


'''For removing product from the Cart'''


class RemoveFromCart(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        Cart.objects.filter(customer=customer, product=product).delete()
        messages.success(request, "Item removed from Cart.")
        return redirect('cart')


'''For adding product to the wishlist if not already exists'''


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


'''For viewing products that are present in the wishlist'''


class WishListView(ListView):
    template_name = 'product/wishlist.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = WishList.objects.filter(customer=Customer.objects.get(user=self.request.user))
        return products


'''For adding a product to the cart if not already exists'''


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


'''For updating the Cart'''


class UpdateCart(View):
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer, product=product)
        cart.quantity = self.request.POST.get('quantity')
        cart.save()
        return redirect('cart')


'''For viewing items in the cart'''


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
        if request.user.is_staff and not request.user.is_superuser:
            products = Product.objects.filter(brand=self.request.user.brand)
            return render(request, 'product/admin_func.html', {'products': products})
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


'''Showing the details of each product'''


class DetailProductView(DetailView):
    model = Product


'''For searching a product based on name, description, brand, category'''


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
