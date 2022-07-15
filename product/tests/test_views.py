import pytest
from django.urls import reverse
from product.models import Cart, WishList, Favourites, Review
from pytest_django.asserts import assertTemplateUsed, assertRedirects
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
    def test_view_page_correctly(self, client, create_customer, create_brand):
        c_user, c_client = create_customer()
        b_user = create_brand()
        b_user_login = client.login(username=b_user.user.username, password='sasshah11@S')
        assert b_user_login
        self.brand_home_url = reverse('view-product')
        self.user_home_url = reverse('grocery_store_home')
        response1 = client.get(self.brand_home_url)
        response2 = c_client.get(self.user_home_url)
        assert response1.status_code == 200
        assertTemplateUsed(response1, 'product/admin_func.html')
        assert response2.status_code == 200
        assertTemplateUsed(response2, 'product/home.html')


class TestAddToCart:
    @pytest.mark.django_db
    def test_view_cart_can_view_page_correctly(self, create_product, create_customer):
        customer, bb = create_customer()
        product = create_product()
        response = bb.get(reverse('add-to-cart', kwargs={'pk': product.id}))
        assertRedirects(response, reverse('cart'), 302, 200)


class TestCartView:
    @pytest.mark.django_db
    def test_view_cart_can_view_page_correctly(self, create_product, create_customer):
        customer, client = create_customer()
        product = create_product()
        cart_obj = Cart.objects.create(customer=customer, product=product, quantity=1)
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
        print(Favourites.objects.all())
        # assert False
        assertRedirects(response, reverse('favourites'), 302, 200)


class TestFavouritesView:
    @pytest.mark.django_db
    def test_view_favourites_can_view_page_correctly(self, create_brand, create_customer):
        customer, client = create_customer()
        brand = create_brand()
        favourites_obj = Favourites.objects.create(customer=customer, brand=brand)
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
        response = bb.post(reverse('add-review', kwargs={'pk': product.id}),{'add_review':review})
        print(Review.objects.all())
        # assert False
        assertRedirects(response, reverse('product-detail'), 302, 200)