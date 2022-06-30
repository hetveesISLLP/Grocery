import django.contrib.messages
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, CustomerRegister, BrandRegister, ProfileUpdateForm, ProfileUpdateFormUser
from django.shortcuts import redirect
from .models import User
from django.views.generic import ListView
from django.contrib.auth.models import Group
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from .models import Customer
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import View


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'store/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('user-profile')


def profile(request):
    user = request.user
    user_details = Customer.objects.filter(user=user).first()
    user_img = user_details.image.url
    customer_form = ProfileUpdateForm(instance=user_details)
    user_form = ProfileUpdateFormUser(instance=user)

    if request.method == 'POST':
        customer_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_details)
        user_form = ProfileUpdateFormUser(request.POST, instance=user)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('user-profile')

    context = {
        'user_form': user_form,
        'customer_form':customer_form,
        'user_img':user_img,
    }

    return render(request, 'store/profile.html', context)


# class UserProfileView(DetailView):
#     # fields - ['username', 'age', 'gender', 'mobile_no', 'email']
#     template_name = 'store/profile.html'
#
#     def get_object(self):
#         print(self.request.user)
#         return self.request.user


class AboutView(TemplateView):
    template_name = "store/about.html"


class FeedbackView(TemplateView):
    template_name = 'store/feedback.html'


def registerbrand(request):
    b_form = BrandRegister()
    u_form = RegistrationForm()

    if request.method == 'POST':

        b_form = BrandRegister(request.POST)
        u_form = RegistrationForm(request.POST)

        if b_form.is_valid() and u_form.is_valid():

            # b_user = b_form.save(commit=False)
            # u_user = u_form.save(commit=False)
            #
            # b_user.brand = b_user.brand.lower()
            # b_user.user = u_user
            # b_user.email = u_user.email

            u_user = u_form.save(commit=False)
            u_user.is_staff = True
            u_user.is_active = False
            u_user.save()
            b_user = b_form.save(commit=False)
            b_user.user = u_user
            b_user.brand = b_user.brand.lower()
            b_form.save()



            # u_user.save()
            # b_user.save()

            brand_admin_privileges = Group.objects.get(name='Brand_admin')
            brand_admin_privileges.user_set.add(u_user)

            messages.success(request, "Successfully created brand")
            return redirect('login')

        else:
            # messages.error(request, "Registration failed.")
            # return redirect('register-brand')
            return render(request, 'store/register_brand.html', {'c_form': b_form, 'u_form': u_form})
    else:
        # messages.error(request, "Invalid Request.")
        return render(request, 'store/register_brand.html', {'c_form': b_form, 'u_form': u_form})


def register(request):
    c_form = CustomerRegister()
    u_form = RegistrationForm()

    if request.method == 'POST':

        c_form = CustomerRegister(request.POST)
        u_form = RegistrationForm(request.POST)

        if c_form.is_valid() and u_form.is_valid():

            # c_user = c_form.save(commit=False)
            u_user = u_form.save()
            c_user = c_form.save(commit=False)
            c_user.user = u_user
            c_form.save()
            # c_user = c_form.save(commit=False)
            # c_user.user = u_user
            # c_user.email = u_user.email
            # c_user.username = u_user.username
            # u_user.save()
            # c_user.save()

            messages.success(request, "Successfully created account")
            return redirect('login')

        else:
            messages.error(request, 'Invalid data. Please try again.')
            # return redirect('register-user')
            return render(request, 'store/register.html', {'c_form': c_form, 'u_form': u_form})

    else:
        return render(request, 'store/register.html', {'c_form': c_form, 'u_form': u_form})







# Permissions
# view, add, change, delete product
# view, change, delete brand