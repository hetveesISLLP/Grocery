from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
# Create your views here.
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import RegistrationForm, CustomerRegister, BrandRegister, ProfileUpdateForm
from django.shortcuts import redirect
from . models import User
from django.views.generic import ListView
from django.contrib.auth.models import Group
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from . models import Customer


def profile(request):
    user = request.user
    user_details = Customer.objects.filter(user=user).first()
    user_form = ProfileUpdateForm(instance=user_details)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=user_details)

        if user_form.is_valid():
            # to add updated data in User table also
            updated_email = user_form.cleaned_data['email']
            updated_username = user_form.cleaned_data['username']
            user_updated = user
            user_updated.email = updated_email
            user_updated.username = updated_username
            user_form.save()
            user_updated.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('grocery_store_home')


    context = {
        'user_form': user_form,
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


class HomeView(ListView):
    template_name = 'store/base.html'
    model = User
    context_object_name = 'users'


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exist !')
            return redirect('login-user')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('grocery_store_home')
        else:
            messages.error(request, 'Invalid Username or password!')
            return redirect('login-user')


    context = {}
    return render(request, 'store/login_user.html', context)


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





