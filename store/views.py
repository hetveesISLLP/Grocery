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


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('grocery_store_home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'store/change_password.html', {
        'form': form
    })


def profile(request):
    user = request.user
    user_details = Customer.objects.filter(user=user).first()
    user_form = ProfileUpdateForm(instance=user_details)
    customer_form = ProfileUpdateFormUser(instance=user)

    if request.method == 'POST':
        customer_form = ProfileUpdateForm(request.POST, instance=user_details)
        user_form = ProfileUpdateFormUser(request.POST, instance=user)

        if user_form.is_valid() and customer_form.is_valid():
            # to add updated data in User table also
            # updated_email = user_form.cleaned_data['email']
            # updated_username = user_form.cleaned_data['username']
            user_updated = user
            # user_updated.email = updated_email
            # user_updated.username = updated_username
            user_form.save()
            user_updated.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('grocery_store_home')

    context = {
        'user_form': user_form,
        'customer_form':customer_form,
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
    template_name = 'store/home.html'
    model = User
    context_object_name = 'users'


# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, 'User Does Not Exist !')
#             return redirect('login')
#
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('grocery_store_home')
#         else:
#             messages.error(request, 'Invalid Username or password!')
#             return redirect('login')
#
#     context = {}
#     return render(request, 'store/login.html', context)


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
            return redirect('admin:index')

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

# def register(request):
#     user_register = SignUpForm()
#     if request.method == 'POST':
#         user_register = SignUpForm(request.POST)
#         if user_register.is_valid():
#             instance = user_register.save()
#             profile_obj = Profile(user=instance)
#             profile_obj.save()
#             messages.success(request, f'Your account has been created! Now you are able to login!!')
#             return redirect('login')
#     else:
#         form = SignUpForm()
#     return render(request, 'users/register.html', {'form': user_register})
