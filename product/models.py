from django.db import models
from django.contrib.auth.models import User
from store.models import Customer, Brand
from django.db.models.fields import IntegerField
import math
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


volume_choices = (
    ("gm", "gm"),
    ("kg", "kg"),
    ("ml", "ml"),
    ("litres", "litres"),
    ("piece", "piece"),
)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    available_quantity = models.IntegerField()
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(upload_to='product_images')
    discount = IntegerField(default=0)
    description = models.TextField(max_length=500)
    no_of_purchases = models.IntegerField(default=0)
    volume = models.FloatField()
    volume_unit = models.CharField(max_length=10, choices=volume_choices, default="gm")

    @property
    def calculate_discount(self):
        if self.discount > 0:
            discounted_price = self.price - self.price * self.discount / 100
            return "{:.2f}".format(discounted_price)
        if self.discount == 0:
            discounted_price = self.price
            return "{:.2f}".format(discounted_price)

    def __str__(self):
        return self.name


class Favourites(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)


class WishList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # many-to-many
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def item_total(self):
        return "{:.2f}".format(float(self.product.calculate_discount) * float(self.quantity))


payment_choices = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Debit Card", "Debit Card"),
    ("Credit Card", "Debit Card"),
    ("UPI", "UPI")
)

status_choices = [
    ("Initialized", "Initialized"),
    ("Packed", "Packed"),
    ("Shipped", "Shipped"),
    ("Reached Distribution Centre", "Reached Distribution Centre"),
    ("Delivered", "Delivered")
]


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # check for Invoice. No need
    address = models.TextField(max_length=200, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=30, choices=payment_choices, default='Card')
    total_amount = models.FloatField()
    # status = models.CharField(max_length=30, choices=status_choices, default="Initialized")
    stripe_payment_intent = models.CharField(max_length=200, null=True)
    has_paid = models.BooleanField(default=False)

    @staticmethod
    def get_orders_by_user(user):
        return Order.objects.filter(customer__user=user).exclude(total_amount=0)


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    status = models.CharField(max_length=30, choices=status_choices, default="Initialized")
    want_return = models.BooleanField(default=False)
    is_picked = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    reason = models.TextField(max_length=500, null=True)

    @property
    def total_price(self):
        return "{:.2f}".format(float(self.product.calculate_discount) * float(self.quantity))
