from .models import Product
from django.views.generic import ListView
from django.views.generic.detail import DetailView


class HomeView(ListView):
    template_name = 'product/home.html'
    model = Product
    context_object_name = 'products'


class DetailProductView(DetailView):
    model = Product



