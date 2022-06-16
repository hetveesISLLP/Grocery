from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image


gender_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=gender_choices, default='Female')
    mobile_no = PhoneNumberField(null=True, unique=True)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            new_size = (300, 300)
            img.thumbnail(new_size)
            img.save(self.image.path)


class Brand(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.brand
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#
#     def __str__(self):
#         return self.name
#
# volume_choices = (
#     ("gm", "gm"),
#     ("kg", "kg"),
#     ("ml", "ml"),
#     ("litres", "litres"),
#     ("piece", "piece"),
# )
#
#
# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     available_quantity = models.IntegerField()
#     name = models.CharField(max_length=50)
#     price = models.FloatField()
#     image = models.ImageField()
#     # todo : default = 0
#     discount = models.IntegerField(default=0)
#     description = models.TextField(max_length=500)
#     # todo : default = 0
#     no_of_purchases = models.IntegerField(default=0)
#     volume = models.FloatField()
#     volume_unit = models.CharField(max_length=10, choices=volume_choices, default="gm")
#
#
#
# class Favourites(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
#
#
# class WishList(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#
#
# class Review(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     review = models.TextField(max_length=300)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#
# class Cart(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     # many-to-many
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#
#
# payment_choices = (
#     ("Cash On Delivery", "Cash On Delivery"),
#     ("Debit Card", "Debit Card"),
#     ("Credit Card", "Debit Card"),
#     ("UPI", "UPI")
# )
#
#
# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     #todo : product, quantity
#     #check for Invoice. No need
#     address = models.TextField(max_length=200)
#     datetime = models.DateTimeField(auto_now_add=True)
#     payment_method = models.CharField(max_length=30, choices=payment_choices, default='Cash On Delivery')
#     total_amount = models.FloatField()
#
#
# class Invoice(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField()


# To be thought for Invoice when product gets deleted.

# class Policy(models.Model):
#     name = models.SlugField(max_length=256, blank=False, unique=True)
# def default_policy():
#     return Policy.objects.get(name='default').pk
# class Item(models.Model):
#     policy = models.ForeignKey('Policy', on_delete=models.SET_DEFAULT, default=default_policy)
# Create your models here.
# Create your models here.
