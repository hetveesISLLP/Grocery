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
        is_logged_in = client.login(username=user.username, password='sasshah11@S')
        assert is_logged_in
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
        is_logged_in = client.login(username=user.username, password='sasshah11@S')
        assert is_logged_in
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


class TestDetailProductView(object):
    """Test for DetailProductView"""

    @pytest.mark.django_db
    def test_detail_product_view(self, create_product):
        product = create_product()
        product_obj = Product.objects.all()
        print("Product", product_obj.values())
        assert product.description == 'Very spicy and tasty'