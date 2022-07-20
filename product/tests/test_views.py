import json

import pytest
from django.urls import reverse
from store.models import Customer, Brand
from product.models import Cart, WishList, Favourites, Review, Product, Category, Order, Invoice
from pytest_django.asserts import assertTemplateUsed, assertRedirects, assertJSONEqual
import uuid


class TestDetailProductView:
    @pytest.mark.django_db
    def test_view_page_correctly(self, client, create_product):
        product = create_product()
        # for Detail Product View
        self.product_detail_url = reverse('product-detail', kwargs={'pk': product.id})
        response = client.get(self.product_detail_url)
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/product_detail.html')


class TestSearchProduct:
    @pytest.mark.django_db
    def test_view_page_correctly(self, client, create_product):
        product1 = create_product()
        product2 = create_product(name='flour', brand='bisleri', p_name='flour 1')
        product3 = create_product(name='biscuits', brand='tata', p_name='flour 2')
        self.product_search_url = reverse('product-search')
        response = client.post(self.product_search_url, {'searched': 'bi'})
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/search.html')


class TestHomeView:
    @pytest.mark.django_db
    def test_view_page_correctly(self, client, create_customer, create_brand, create_product):
        p1 = create_product()
        p2 = create_product()

        c_user, c_client = create_customer()
        self.user_home_url = reverse('grocery_store_home')
        response2 = c_client.get(self.user_home_url)
        assert response2.status_code == 200
        assertTemplateUsed(response2, 'product/home.html')

        b_user = create_brand()
        b_user_login = client.login(username=b_user.user.username, password='sasshah11@S')
        assert b_user_login
        self.brand_home_url = reverse('grocery_store_home')
        response1 = client.get(self.brand_home_url)
        assert response1.status_code == 200
        assertTemplateUsed(response1, 'product/admin_func.html')


class TestAddToCart:
    @pytest.mark.django_db
    def test_view_cart_can_view_page_correctly(self, create_product, create_customer):
        customer, bb = create_customer()
        product = create_product()
        response = bb.get(reverse('add-to-cart', kwargs={'pk': product.id}))
        response2 = bb.get(reverse('add-to-cart', kwargs={'pk': product.id}), follow=True)
        messages = list(response2.context['messages'])

        assert str(messages[1]) == 'Item Already exist in cart'
        assertRedirects(response, reverse('cart'), 302, 200)


class TestCartView:
    @pytest.mark.django_db
    def test_view_cart_can_view_page_correctly(self, create_product, create_customer):
        customer1, client = create_customer()

        product = create_product()
        cart_obj = Cart.objects.create(customer=customer1, product=product, quantity=1)
        cart_obj2 = Cart.objects.create(customer=customer1, product=product, quantity=1)
        self.cart_url = reverse('cart')
        response = client.get(self.cart_url)
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/add_to_cart.html')


class TestUpdateCart:
    @pytest.mark.django_db
    def test_update_cart_can_view_page_correctly(self, create_product, create_customer):
        customer, client = create_customer()
        product = create_product()
        cart_obj = Cart.objects.create(customer=customer, product=product, quantity=1)
        self.cart_update_url = reverse('update-cart', kwargs={'pk': product.id})
        response = client.post(self.cart_update_url, {'quantity': 7})
        print(Cart.objects.all().values())
        assertRedirects(response, reverse('cart'), 302, 200)


class TestRemoveFromCart:
    @pytest.mark.django_db
    def test_remove_cart_can_view_page_correctly(self, create_product, create_customer):
        customer, client = create_customer()
        product = create_product()
        cart_obj = Cart.objects.create(customer=customer, product=product, quantity=1)
        # print(Cart.objects.all().values())
        self.remove_from_cart_url = reverse('remove-from-cart', kwargs={'pk': product.id})
        response = client.get(self.remove_from_cart_url, {'pk': product.id})
        # print(Cart.objects.all().values())
        assertRedirects(response, reverse('cart'), 302, 200)


class TestAddToWishList:
    @pytest.mark.django_db
    def test_add_to_wishlist_can_view_page_correctly(self, create_product, create_customer):
        customer, bb = create_customer()
        product = create_product()
        response = bb.get(reverse('add-to-wishlist', kwargs={'pk': product.id}))
        response2 = bb.get(reverse('add-to-wishlist', kwargs={'pk': product.id}), follow=True)
        messages = list(response2.context['messages'])

        assert str(messages[1]) == 'Item Already exist'
        print(WishList.objects.all())
        # assert False
        assertRedirects(response, reverse('wishlist'), 302, 200)


class TestWishListView:
    @pytest.mark.django_db
    def test_view_wishlist_can_view_page_correctly(self, create_product, create_customer):
        customer, client = create_customer()
        product = create_product()
        wishList_obj = WishList.objects.create(customer=customer, product=product)
        self.wishlist_url = reverse('wishlist')
        response = client.get(self.wishlist_url)
        print(WishList.objects.all())
        # assert False
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/wishlist.html')


class TestRemoveFromWishList:
    @pytest.mark.django_db
    def test_remove_wishlist_can_view_page_correctly(self, create_product, create_customer):
        customer, client = create_customer()
        product = create_product()
        wishlist_obj = WishList.objects.create(customer=customer, product=product)
        print(WishList.objects.all().values())
        self.remove_from_wishlist_url = reverse('remove-from-wishlist', kwargs={'pk': product.id})
        response = client.get(self.remove_from_wishlist_url, {'pk': product.id})
        print(Cart.objects.all().values())
        # assert False
        assertRedirects(response, reverse('wishlist'), 302, 200)


class TestAddToFavourites:
    @pytest.mark.django_db
    def test_add_to_favourites_can_view_page_correctly(self, create_brand, create_customer):
        customer, bb = create_customer()
        brand = create_brand()
        response = bb.get(reverse('add-to-favourites', kwargs={'pk': brand.id}))
        response2 = bb.get(reverse('add-to-favourites', kwargs={'pk': brand.id}), follow=True)
        print(Favourites.objects.all())
        assertRedirects(response, reverse('favourites'), 302, 200)
        assertRedirects(response2, reverse('favourites'), 302, 200)
        # print(response.context['messages'])
        # print(response2.context['messages'])
        messages = list(response2.context['messages'])
        # assert len(messages) == 1
        assert str(messages[1]) == 'Brand Already exist in Favourites'


class TestFavouritesView:
    @pytest.mark.django_db
    def test_view_favourites_can_view_page_correctly(self, create_brand, create_customer):
        customer, client = create_customer()
        brand = create_brand()
        b2 = create_brand()
        favourites_obj = Favourites.objects.create(customer=customer, brand=brand)
        favourites_obj2 = Favourites.objects.create(customer=customer, brand=b2)
        self.favourites_url = reverse('favourites')
        response = client.get(self.favourites_url)
        print(Favourites.objects.all())
        # assert False
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/favourites.html')


class TestRemoveFromFavourites:
    @pytest.mark.django_db
    def test_remove_favourites_can_view_page_correctly(self, create_brand, create_customer):
        customer, client = create_customer()
        brand = create_brand()
        favourites_obj = Favourites.objects.create(customer=customer, brand=brand)
        print(Favourites.objects.all().values())
        self.remove_from_favourites_url = reverse('remove-from-favourites', kwargs={'pk': brand.id})
        response = client.get(self.remove_from_favourites_url, {'pk': brand.id})
        print(Favourites.objects.all().values())
        # assert False
        assertRedirects(response, reverse('favourites'), 302, 200)


class TestAddReview:
    @pytest.mark.django_db
    def test_add_review_can_view_page_correctly(self, create_product, create_customer):
        customer, bb = create_customer()
        product = create_product()
        review = 'very good product'
        response = bb.post(reverse('add-review', kwargs={'pk': product.id}), {'add_review': review})
        print(Review.objects.all())
        # assert False
        assertRedirects(response, reverse('product-detail', kwargs={'pk': product.id}), 302, 200)


class TestCategoryView:
    @pytest.mark.django_db
    def test_category_view_view_page_correctly(self, create_category, create_customer, create_product):
        c2 = create_category(name='flour')
        customer, client = create_customer()
        p2 = create_product(name=c2)
        p3 = create_product()
        # print(Product.objects.filter(category=c2.id))
        response = client.get(reverse('view-category', kwargs={'category': c2.name}))
        response.status_code == 200
        assertTemplateUsed(response, 'product/filter_result.html')


class TestFilterProduct:
    @pytest.mark.django_db
    def test_can_view_page(self, create_product, create_customer):
        customer, client = create_customer()
        p1 = create_product(p_name='flower')
        p1 = create_product(p_name='faun')
        min = 100
        max = 200
        self.product_filter_url = reverse('price-filter')
        response = client.get(self.product_filter_url, {'min_val': min, 'max_val': max})
        assertTemplateUsed(response, 'product/filter_result.html')
        response.status_code == 200
        print(Product.objects.filter(price__gte=float(min), price__lte=float(max)))


class TestAddCategory:
    @pytest.mark.django_db
    def test_can_view_page(self, create_brand, client, create_category):
        b = create_brand()
        c = create_category(name='drinks')
        brand_login = client.login(username=b.user.username, password='sasshah11@S')
        response = client.post(reverse('add-category'))
        print(Category.objects.all())
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/add_category.html')


class TestUpdateBrandName:
    @pytest.mark.django_db
    def test_can_view_page(self, create_brand, client):
        brand = create_brand(brand='bikaji')
        brand_login = client.login(username=brand.user.username, password='sasshah11@S')
        response = client.get(reverse('update-brand_name', kwargs={'pk': brand.id}))
        assertTemplateUsed(response, 'product/update_brand_name.html')
        assert response.status_code == 200
        # print(Brand.objects.all())
        response = client.post(reverse('update-brand_name', kwargs={'pk': brand.id}), {'brand': 'Lalaji'})
        # print(Brand.objects.all())
        assertRedirects(response, reverse('grocery_store_home'), 302, 200)


class TestAddProductView:

    @pytest.mark.django_db
    def test_can_view_page(self, create_brand, create_category, client):
        b = create_brand()
        c = create_category(name='gopal')
        b_login = client.login(username=b.user.username, password='sasshah11@S')
        response = client.get(reverse('add-product', kwargs={'pk': b.id}))
        assertTemplateUsed(response, 'product/add_product.html')
        assert response.status_code == 200
        print(Product.objects.all())
        response = client.post(reverse('add-product', kwargs={'pk': b.id}), {
            'name': 'chokdi',
            'price': 100,
            'description': 'nice',
            'available_quantity': 100,
            'discount': 10,
            'category': c.id,
            'volume': 1,
            'volume_unit': 'kg'
        })
        print(Product.objects.all())
        assertRedirects(response, reverse('grocery_store_home'), 302, 200)


class TestUpdateProductView:
    @pytest.mark.django_db
    def test_can_view_page(self, create_brand, create_category, client):
        b = create_brand(brand='poly')
        c = create_category(name='snacks')
        b_login = client.login(username=b.user.username, password='sasshah11@S')
        p = Product.objects.create(
            name='chokdi',
            description='good',
            price=100,
            available_quantity=10,
            discount=3,
            volume_unit='kg',
            volume=1,
            category=c,
            brand=b
        )
        response = client.get(reverse('update-product', kwargs={'pk': p.id}))
        assertTemplateUsed(response, 'product/update_product.html')
        assert response.status_code == 200
        # print(Product.objects.filter(pk=p.id).values())
        response = client.post(reverse('update-product', kwargs={'pk': p.id}),
                               {
                                   'name': 'poprings',
                                   'description': 'sweet',
                                   'quantity': 80,
                                   'price': p.price,
                                   'available_quantity': p.available_quantity,
                                   'discount': p.discount,
                                   'volume': p.volume,
                                   'volume_unit': p.volume_unit,
                                   'category': p.category.id
                               })
        # print(Product.objects.filter(pk=p.id).values())
        assertRedirects(response, reverse('grocery_store_home'), 302, 200)


class TestViewCheckout:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer):
        c, client = create_customer()
        response = client.get(reverse('view-checkout'))
        assertTemplateUsed(response, 'product/view_checkout.html')
        assert response.status_code == 200


class TestOnlyAddress:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer):
        c, client = create_customer()
        response = client.get(reverse('buy-now-cart'))
        assertTemplateUsed(response, 'product/only_address.html')
        assert response.status_code == 200


class TestCreateCheckoutSessionCart:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer, create_product):
        c, client = create_customer()
        p1 = create_product(name='poly')
        p2 = create_product(name='holy')
        cart1 = Cart.objects.create(customer=c, product=p1, quantity=3)
        cart2 = Cart.objects.create(customer=c, product=p2, quantity=2)
        data = {'address-buy': 'rajkot'}
        response2 = client.post(reverse('checkout-address'), json.dumps(data), content_type='application/json')
        # print(response2.context['sessionId'])
        # print(json.loads(response2.content))
        # session = json.loads(response2.content).get('sessionId', None)
        # assert session
        # a = Order.objects.all()
        # print(a.values())
        # assert False
        p3 = create_product(name='poly')
        p4 = create_product(name='holy')
        cart12 = Cart.objects.create(customer=c, product=p3, quantity=90)
        cart22 = Cart.objects.create(customer=c, product=p4, quantity=90)
        data = {'address-buy': 'rajkot'}
        response3 = client.post(reverse('checkout-address'), json.dumps(data), content_type='application/json')
        # print(response2.context['sessionId'])
        # print(json.loads(response3.content))
        # session = json.loads(response3.content).get('sessionId', None)
        # assert session
        assertJSONEqual(
            str(response3.content, encoding='utf8'),
            {'message': False}
        )


# cant test for this as payment wont be successful
class TestPaymentSuccessViewCart:
    pass


class TestOrderDetailsView:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer, create_product):
        c, client = create_customer()
        p = create_product()
        response = client.get(reverse('buy-now', kwargs={'pk': p.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/buy_address.html')


class TestCreateCheckoutSession:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer, create_product):
        c, client = create_customer()
        p1 = create_product(name='poly')
        data = {'address-buy': 'rajkot', 'quantityy': 2}
        response1 = client.post(reverse('api_checkout_session', kwargs={'pk': p1.id}), json.dumps(data),
                                content_type='application/json')
        # print(response2.context['sessionId'])
        # print(json.loads(response2.content))
        session = json.loads(response1.content).get('sessionId', None)
        assert session
        # a = Order.objects.all()
        # print(a.values())
        p2 = create_product(name='polo')
        data = {'address-buy': 'rajkot', 'quantityy': 90}
        response2 = client.post(reverse('api_checkout_session', kwargs={'pk': p1.id}), json.dumps(data),
                                content_type='application/json')
        assertJSONEqual(
            str(response2.content, encoding='utf8'),
            {'message': False}
        )


# cant test for this as payment wont be successful
class TestPaymentSuccessView:
    pass


class TestPurchasedView:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer, create_product):
        c, client = create_customer()
        p = create_product()
        o = Order.objects.create(customer=c, address='kikik', total_amount=100.00, stripe_payment_intent='hello')
        i = Invoice.objects.create(order=o, product=p, quantity=4)
        response = client.get(reverse('orders'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/view_purchased.html')


class TestDetailPurchasedView:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer, create_product):
        c, client = create_customer()
        p = create_product()
        o = Order.objects.create(customer=c, address='kikik', total_amount=100.00, stripe_payment_intent='hello')
        i = Invoice.objects.create(order=o, product=p, quantity=4)
        response = client.get(reverse('detail-orders', kwargs={'pk': o.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/detail_order.html')


class TestDownloadInvoice:
    pass


class TestProductView:
    @pytest.mark.django_db
    def test_can_view_page(self, create_product, create_brand, client, create_category):
        b = create_brand(brand='sofo')
        c = create_category()
        p1 = create_product()
        p2 = Product.objects.create(
            category=c,
            brand=b,
            available_quantity=5,
            name='jira',
            price=200,
            image='/home/hetvi/Downloads/download.jpeg',
            discount=1,
            description='Very spicy and tasty',
            volume=1,
            volume_unit='kg',
            no_of_purchases=0
        )
        b_login = client.login(username=b.user.username, password='sasshah11@S')
        response = client.get(reverse('view-product'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/admin_func.html')


class TestViewOrdersVendor:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer, create_brand, create_product, client):
        b = create_brand()
        c, clien = create_customer()
        p1 = create_product()
        p2 = Product.objects.create(
            category=p1.category,
            brand=b,
            available_quantity=5,
            name='jira',
            price=200,
            image='/home/hetvi/Downloads/download.jpeg',
            discount=1,
            description='Very spicy and tasty',
            volume=1,
            volume_unit='kg',
            no_of_purchases=0
        )

        b_login = client.login(username=b.user.username, password='sasshah11@S')
        o = Order.objects.create(customer=c, address='kikik', total_amount=100.00, stripe_payment_intent='hello')
        i = Invoice.objects.create(order=o, product=p2, quantity=4)
        response = client.get(reverse('view-order'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/view_order_vendor.html')


class TestUpdateOrderStatus:
    @pytest.mark.django_db
    def test_can_view_page(self, create_brand, create_customer, create_product, client, create_category):
        c, clien = create_customer()
        cat = create_category()
        b = create_brand(brand='sofo')
        p1 = Product.objects.create(
            category=cat,
            brand=b,
            available_quantity=5,
            name='sira',
            price=200,
            image='/home/hetvi/Downloads/download.jpeg',
            discount=1,
            description='Very spicy and tasty',
            volume=1,
            volume_unit='kg',
            no_of_purchases=0
        )

        p2 = Product.objects.create(
            category=cat,
            brand=b,
            available_quantity=5,
            name='jira',
            price=200,
            image='/home/hetvi/Downloads/download.jpeg',
            discount=1,
            description='Very spicy and tasty',
            volume=1,
            volume_unit='kg',
            no_of_purchases=0
        )
        'product/update_order_status.html'
        b_login = client.login(username=b.user.username, password='sasshah11@S')
        o = Order.objects.create(customer=c, address='kikik', total_amount=100.00, stripe_payment_intent='hello')
        i = Invoice.objects.create(order=o, product=p2, quantity=4)
        response = client.get(reverse('update-product-status', kwargs={'pk': i.id}))
        assert response.status_code == 200
        print(Invoice.objects.all().values())
        assertTemplateUsed(response, 'product/update_order_status.html')
        response = client.post(reverse('update-product-status', kwargs={'pk': i.id}), {'status': 'Packed'})
        print(Invoice.objects.all().values())
        assertRedirects(response, reverse('view-order'), 302, 200)


class TestReturnProductView:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer, create_brand, create_product):
        c, client = create_customer()
        p2 = create_product()

        # b_login = client.login(username=b.user.username, password='sasshah11@S')
        o = Order.objects.create(customer=c, address='kikik', total_amount=100.00, stripe_payment_intent='hello')
        i = Invoice.objects.create(order=o, product=p2, quantity=4)

        response = client.get(reverse('return-product', kwargs={'pk': i.id}))
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/return.html')


class TestReturnStatus:
    @pytest.mark.django_db
    def test_can_view_page(self, create_customer, create_brand, create_product):
        b = create_brand(brand='sopo')
        c, client = create_customer()
        p2 = create_product()

        # b_login = client.login(username=b.user.username, password='sasshah11@S')
        o = Order.objects.create(customer=c, address='kikik', total_amount=100.00, stripe_payment_intent='hello')
        i = Invoice.objects.create(order=o, product=p2, quantity=4)
        response = client.post(reverse('return-status', kwargs={'pk': i.id}), {'return': 'bad design'})
        assertRedirects(response, reverse('orders'), 302, 200)


class TestFailureView:
    def test_can_view_page(self, create_customer):
        c, client = create_customer()
        response = client.get(reverse('failure'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'product/failure_payment.html')
