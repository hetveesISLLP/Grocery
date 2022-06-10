from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
# Create your views here.
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import RegistrationForm, CustomerRegister, BrandRegister
from django.shortcuts import redirect
from . models import User
from django.views.generic import ListView
from django.contrib.auth.models import Group


def aboutus(request):
    return render(request, 'store/about.html')

def contactus(request):
    return render(request, 'store/contact.html')

def givefeedback(request):
    messages.success(request, f"Feedback page")
    return render(request, 'store/feedback.html')

class HomeView(ListView):
    template_name = 'store/base.html'
    model = User
    context_object_name = 'users'


def registerbrand(request):
    b_form = BrandRegister()
    u_form = RegistrationForm()

    if request.method == 'POST':

        b_form = BrandRegister(request.POST)
        u_form = RegistrationForm(request.POST)

        if b_form.is_valid() and u_form.is_valid():

            b_user = b_form.save(commit=False)
            u_user = u_form.save(commit=False)

            b_user.brand = b_user.brand.lower()
            b_user.user = u_user
            b_user.email = u_user.email

            u_user.is_staff = True

            u_user.save()
            b_user.save()

            brand_admin_privileges = Group.objects.get(name='Brand_admin')
            brand_admin_privileges.user_set.add(u_user)

            messages.success(request, "Successfully created brand")
            return redirect('admin:index')

        else:
            messages.error(request, "Registration failed.")
            return redirect('register-brand')
    else:
        messages.error(request, "Invalid Request.")
        return render(request, 'store/register.html', {'c_form': b_form, 'u_form': u_form})


def register(request):

    c_form = CustomerRegister()
    u_form = RegistrationForm()

    if request.method == 'POST':

        c_form = CustomerRegister(request.POST)
        u_form = RegistrationForm(request.POST)

        if c_form.is_valid() and u_form.is_valid():

            c_user = c_form.save(commit=False)
            u_user = u_form.save(commit=False)
            c_user.user = u_user
            c_user.email = u_user.email
            c_user.username = u_user.username

            u_user.save()
            c_user.save()

            messages.success(request, "Successfully created account")
            return redirect('login-user')

        else:
            messages.error(request, "Registration failed.")
            return HttpResponse("Registration Failed.")
    else:
        messages.error(request, "Invalid Request.")
        return render(request, 'store/register.html', {'c_form': c_form, 'u_form': u_form})

