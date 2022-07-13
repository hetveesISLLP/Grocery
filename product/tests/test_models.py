import pytest
from product.models import Category, Product, Order, Invoice, Favourites, WishList, Cart, Review
from store.models import Customer, Brand
from django.contrib.auth.models import User


@pytest.fixture
def create_customer(db, client):
    # This fixture creates user+customer and logs them in
    def make_user():
        user = User.objects.create_user(username='sasa', password='sasshah11@S')
        user.email = 'sas@gmail.com'
        user.save()
        customer = Customer.objects.create(user=user, mobile_no='+911234312354', age=23, gender="Female")
        is_logged_in = client.login(username=user.username, password='sasshah11@S')
        assert is_logged_in
        return client, customer
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
        return client, brand
    return make_user


@pytest.fixture
def create_category(db, client):
    # This fixture creates category
    def make_category():
        category = Category.objects.create(category='bhujia')
        return client, category
    return make_category

class TestProductModel(object):
    @pytest.mark.django_db
    def test_field_value(self, create_brand, create_category):
        category = create_category()
        brand = create_brand()



#         manager = create_role_based_user(name='manager', email='desaiparth@gmail.com')
#         obj = create_manager_comment_obj(post=post, manager=manager, comment='Comment Content')
#
#         assert obj.post == post
#         assert obj.manager == manager
#         assert obj.comment == 'Comment Content'
