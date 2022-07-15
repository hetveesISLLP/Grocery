import pytest
from store.models import Customer, Brand
from django.contrib.auth.models import User


# @pytest.fixture
# def create_customer(db, client):
#     # This fixture creates user+customer and logs them in
#     def make_user():
#         user = User.objects.create_user(username='nana', password='nanshah11@N')
#         user.email = 'nana@gmail.com'
#         user.save()
#         customer = Customer.objects.create(user=user, mobile_no='+911234312354', age=23, gender="Female")
#         # is_logged_in = client.login(username=user.username, password='sasshah11@S')
#         # assert is_logged_in
#         return customer
#
#     return make_user
#
#
# @pytest.fixture
# def create_brand(db, client):
#     # This fixture creates user+brand and logs them in
#     def make_user():
#         user = User.objects.create_user(username='sasa', password='sasshah11@S')
#         user.email = 'sas@gmail.com'
#         user.save()
#         brand = Brand.objects.create(user=user, brand='bikaji')
#         brand.user.is_active = True
#         # is_logged_in = client.login(username=user.username, password='sasshah11@S')
#         # assert is_logged_in
#         return brand
#
#     return make_user


class TestCustomerModel(object):
    """Test case for Customer Model"""

    def test_field_value(self, create_customer):
        new_customer = create_customer()
        customer_view = Customer.objects.all()
        print("Customer", customer_view.values())
        assert new_customer.user.username == 'nana'
        assert new_customer.user.email == 'nana@gmail.com'
        assert new_customer.age == 23


class TestBrandModel(object):
    """Test case for Brand Model"""

    def test_field_value(self, create_brand):
        new_brand = create_brand()
        brand_view = Brand.objects.all()
        print('Brand', brand_view.values())
        assert new_brand.user.username == 'sasa'
        assert new_brand.user.email == 'sas@gmail.com'
        assert new_brand.brand == 'bikaji'
