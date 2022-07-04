from django import forms
# from forms import
from .models import Order
status_choices = [
    ("Initialized", "Initialized"),
    ("Packed", "Packed"),
    ("Shipped", "Shipped"),
    ("Reached Distribution Centre", "Reached Distribution Centre"),
    ("Delivered", "Delivered")
]


class UpdateStatus(forms.ModelForm):

    status = forms.CharField(max_length=30, choices=status_choices, default="Initialized")

    class Meta:
        model = Order
        fields = ['status']




