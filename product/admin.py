from django.contrib import admin
from . models import WishList, Cart, Category, Invoice, Order, Review, Favourites, Product

admin.site.register(WishList)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Favourites)


class ProductModify(admin.ModelAdmin):

    readonly_fields = ('brand',)

    def get_queryset(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            # Product.brand = request.user.brand
            return Product.objects.filter(brand=request.user.brand)
        else:
            # Product.brand = request.user.brand
            return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        if request.user.is_staff and not request.user.is_superuser:
            obj.brand = request.user.brand
            obj.last_modified_by = request.user.brand
            obj.save()
        else:
            obj.save()


admin.site.register(Product, ProductModify)

