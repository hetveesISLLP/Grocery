import pytest
from product.models import Category, Product, Order, Invoice, Favourites, WishList, Cart, Review
from store.models import Customer, Brand
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRedirects
import uuid


@pytest.fixture
def create_customer(db, client):
    # This fixture creates user+customer and logs them in
    def make_user(username=None, email=None, mobile_no=None):
        if username is None:
            username = 'user2'
        if email is None:
            email = 'user2@gmail.com'
        if mobile_no is None:
            mobile_no = '+909089899090'

        user = User.objects.create_user(username=username, password='nanshah11@N')
        user.email = email
        user.save()
        customer = Customer.objects.create(user=user, mobile_no=mobile_no, age=23, gender="Female")
        is_logged_in = client.login(username=user.username, password='nanshah11@N')

        assert is_logged_in
        return customer, client

    return make_user


@pytest.fixture
def create_brand(db):
    # This fixture creates user+brand and logs them in
    def make_user(username=None, email=None, brand=None):
        if username is None:
            username = str(uuid.uuid4())
        if email is None:
            email = 'email1@gmail.com'
        if brand is None:
            brand = str(uuid.uuid4())
        user = User.objects.create_user(username=username, password='sasshah11@S')
        user.email = email
        user.save()
        new_brand = Brand.objects.create(user=user, brand=brand)
        new_brand.user.is_active = True
        # is_logged_in = client.login(username=user.username, password='sasshah11@S')
        # assert is_logged_in
        return new_brand

    return make_user


@pytest.fixture
def create_category(db, client):
    """Fixture for creating category"""

    def make_category(name=None):
        if name is None:
            name = str(uuid.uuid4())
        new_category, flag = Category.objects.get_or_create(name=name)
        return new_category

    return make_category


@pytest.fixture
def create_product(db, create_category, create_brand):
    """Fixture for creating category+brand+brand_login+product"""

    def make_product(name=None, brand=None, p_name=None):
        new_brand = create_brand(brand=brand)
        new_category = create_category(name=name)
        if p_name is None:
            p_name = str(uuid.uuid4())
        product = Product.objects.create(
            category=new_category,
            brand=new_brand,
            available_quantity=5,
            name=p_name,
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

