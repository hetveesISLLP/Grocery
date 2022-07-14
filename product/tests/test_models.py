import pytest
from product.models import Category, Product, Order, Invoice, Favourites, WishList, Cart, Review
from store.models import Customer, Brand
from django.contrib.auth.models import User


@pytest.fixture
def create_customer(db, client):
    # This fixture creates user+customer and logs them in
    def make_user():
        user = User.objects.create_user(username='nana', password='nanshah11@N')
        user.email = 'nana@gmail.com'
        user.save()
        customer = Customer.objects.create(user=user, mobile_no='+911234312354', age=23, gender="Female")
        # is_logged_in = client.login(username=user.username, password='sasshah11@S')
        # assert is_logged_in
        return customer

    return make_user


@pytest.fixture
def create_brand(db, client):
    # This fixture creates user+brand and logs them in
    def make_user():
        user = User.objects.create_user(username='sasa', password='sasshah11@S')
        user.email = 'sas@gmail.com'
        user.save()
        brand = Brand.objects.create(user=user, brand='bikaji')
        brand.user.is_active = True
        # is_logged_in = client.login(username=user.username, password='sasshah11@S')
        # assert is_logged_in
        return brand

    return make_user


@pytest.fixture
def create_category(db, client):
    """Fixture for creating category"""

    def make_category():
        category = Category.objects.create(name='bhujia')
        return category

    return make_category


@pytest.fixture
def create_product(db, create_category, create_brand):
    """Fixture for creating category+brand+brand_login+product"""

    def make_product():
        new_brand = create_brand()
        new_category = create_category()
        product = Product.objects.create(
            category=new_category,
            brand=new_brand,
            available_quantity=5,
            name='Bikaneri',
            price=200,
            image='/home/hetvi/Downloads/download.jpeg',
            discount=10,
            description='Very spicy and tasty',
            volume=1,
            volume_unit='kg',
            no_of_purchases=0
        )
        return product

    return make_product


class TestOrderModel(object):
    """Test case for Order Model"""

    def test_field_value(self, create_customer):
        new_customer = create_customer()
        order_obj = Order.objects.create(customer=new_customer, address='rajkot', total_amount=300)
        order_view = Order.objects.all()
        print("Order", order_view.values())
        assert order_obj.customer == new_customer
        assert order_obj.address == 'rajkot'
        assert order_obj.total_amount == 300


class TestInvoiceModel(object):
    """Test case for Invoice Model"""

    def test_field_value(self, create_product, create_customer):
        new_product = create_product()
        new_customer = create_customer()
        order_obj = Order.objects.create(customer=new_customer, address='rajkot', total_amount=300)
        invoice_obj = Invoice.objects.create(order=order_obj, product=new_product, quantity=4)
        invoice_view = Invoice.objects.all()
        print("Invoice", invoice_view.values())
        assert invoice_obj.order.customer == new_customer
        assert invoice_obj.order == order_obj
        assert invoice_obj.product == new_product
        assert invoice_obj.quantity == 4


class TestFavouritesModel(object):
    """Test case for Favourites Model"""

    def test_field_value(self, create_brand, create_customer):
        new_brand = create_brand()
        new_customer = create_customer()
        favourites_obj = Favourites.objects.create(brand=new_brand, customer=new_customer)
        favourites_view = Favourites.objects.all()
        print("Favourites", favourites_view.values())
        assert favourites_obj.customer == new_customer
        assert favourites_obj.brand == new_brand


class TestWishListModel(object):
    """Test case for WishList Model"""

    def test_field_value(self, create_customer, create_product):
        new_customer = create_customer()
        new_product = create_product()
        wishlist_obj = WishList.objects.create(customer=new_customer, product=new_product)
        wishlist_view = WishList.objects.all()
        print("Wishlist", wishlist_view.values())
        assert wishlist_obj.customer == new_customer
        assert wishlist_obj.product == new_product


class TestCartModel(object):
    """Test for Cart Model"""

    def test_field_value(self, create_customer, create_product):
        new_customer = create_customer()
        new_product = create_product()
        cart_obj = Cart.objects.create(customer=new_customer, product=new_product, quantity=5)
        cart_view = Cart.objects.all()
        print("Cart", cart_view.values())
        assert cart_obj.customer == new_customer
        assert cart_obj.product == new_product
        assert cart_obj.quantity == 5


class TestReviewModel(object):
    """Test for Review Model"""

    def test_field_value(self, create_product, create_customer):
        new_product = create_product()
        new_customer = create_customer()
        review = Review.objects.create(customer=new_customer, product=new_product, review='very good')
        view_review = Review.objects.all()
        print("Review", view_review.values())
        assert review.product == new_product
        assert review.customer == new_customer
        assert review.review == 'very good'


class TestProductModel(object):
    """Test for Product Model"""

    @pytest.mark.django_db
    def test_field_value(self, create_product):
        product = create_product()
        product_obj = Product.objects.all()
        print("Product", product_obj.values())
        assert product.description == 'Very spicy and tasty'


class TestCategoryModel(object):
    """Test for Category Model"""

    @pytest.mark.django_db
    def test_field_value(self, create_category):
        new_category = create_category()
        print("category", new_category)
        assert new_category.name == 'bhujia'
