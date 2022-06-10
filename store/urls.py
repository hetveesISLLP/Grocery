from . views import HomeView, register, registerbrand
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name="grocery_store_home"),
    path('register/', register, name='register-user'),
    path('brand-register/', registerbrand, name="register-brand"),
    # path('about/', aboutus, name='about-us'),
    # path('contact/', include('store/contact.html'), name='contact-us'),
    # path('feedback/', include('store/feedback.html'), name='feedback-us'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login-user'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout-user'),


]