import pytest
from product.models import Category, Product, Order, Invoice, Favourites, WishList, Cart, Review
from store.models import Customer, Brand
from django.contrib.auth.models import User


class TestOrderModel(object):
    """Test case for Order Model"""

    def test_field_value(self, create_customer):
        new_customer, client = create_customer()
        order_obj1 = Order.objects.create(customer=new_customer, address='rajkot', total_amount=300)
        order_obj2 = Order.objects.create(customer=new_customer, address='porbander', total_amount=100)
        # order_view = Order.objects.all()
        # print("Order", order_view.values())
        assert order_obj1.customer == new_customer
        assert order_obj1.address == 'rajkot'
        assert order_obj1.total_amount == 300
        # assert order_obj2.customer == new_customer
        # assert order_obj2.address == 'porbander'
        # assert order_obj2.total_amount == 100



class TestInvoiceModel(object):
    """Test case for Invoice Model"""

    def test_field_value(self, create_product, create_customer):
        new_product = create_product()
        new_customer, client = create_customer()
        order_obj = Order.objects.create(customer=new_customer, address='rajkot', total_amount=300)
        invoice_obj = Invoice.objects.create(order=order_obj, product=new_product, quantity=4)
        invoice_view = Invoice.objects.all()
        print("Invoice", invoice_view.values())
        assert invoice_obj.order.customer == new_customer
        assert invoice_obj.order == order_obj
        assert invoice_obj.product == new_product
        assert invoice_obj.quantity == 4
        assert invoice_obj.total_price == '720.00'


class TestFavouritesModel(object):
    """Test case for Favourites Model"""

    def test_field_value(self, create_brand, create_customer):
        new_brand = create_brand()
        new_customer, client = create_customer()
        favourites_obj = Favourites.objects.create(brand=new_brand, customer=new_customer)
        favourites_view = Favourites.objects.all()
        print("Favourites", favourites_view.values())
        assert favourites_obj.customer == new_customer
        assert favourites_obj.brand == new_brand


class TestWishListModel(object):
    """Test case for WishList Model"""

    def test_field_value(self, create_customer, create_product):
        new_customer, client = create_customer()
        new_product = create_product()
        wishlist_obj = WishList.objects.create(customer=new_customer, product=new_product)
        wishlist_view = WishList.objects.all()
        print("Wishlist", wishlist_view.values())
        assert wishlist_obj.customer == new_customer
        assert wishlist_obj.product == new_product


class TestCartModel(object):
    """Test for Cart Model"""

    def test_field_value(self, create_customer, create_product):
        new_customer, client = create_customer()
        new_product = create_product()
        cart_obj = Cart.objects.create(customer=new_customer, product=new_product, quantity=5)
        cart_view = Cart.objects.all()
        print("Cart", cart_view.values())
        assert cart_obj.customer == new_customer
        assert cart_obj.product == new_product
        assert cart_obj.quantity == 5
        assert cart_obj.item_total() == '900.00'




class TestReviewModel(object):
    """Test for Review Model"""

    def test_field_value(self, create_product, create_customer):
        new_product = create_product()
        new_customer, client = create_customer()
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
        product = create_product(p_name='polo')
        # product_obj = Product.objects.all()
        # print("Product", product_obj.values())
        assert product.description == 'Very spicy and tasty'
        assert product.calculate_discount == '180.00'
        assert str(product) == 'polo'

        product2 = create_product(p_discount=0)
        assert product2.description == 'Very spicy and tasty'
        assert product2.calculate_discount == '200.00'



class TestCategoryModel(object):
    """Test for Category Model"""

    @pytest.mark.django_db
    def test_field_value(self, create_category):
        new_category = create_category(name='bhujia')
        print("category", new_category)
        assert new_category.name == 'bhujia'
