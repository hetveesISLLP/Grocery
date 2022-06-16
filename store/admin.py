from django.contrib import admin
from . models import Customer, Brand
admin.site.register(Customer)


class BrandModify(admin.ModelAdmin):
    readonly_fields = ('user',)

    def get_queryset(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            Brand.user = request.user
            return Brand.objects.filter(user=request.user)
        else:
            Brand.user = request.user
            return super().get_queryset(request)


admin.site.register(Brand, BrandModify)

