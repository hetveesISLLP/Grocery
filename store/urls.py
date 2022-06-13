from . views import HomeView, register, registerbrand, FeedbackView, AboutView, loginPage, profile
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('', HomeView.as_view(), name="grocery_store_home"),
    path('register/', register, name='register-user'),
    path('brand-register/', registerbrand, name="register-brand"),
    path('about/', AboutView.as_view(), name='about-us'),
    path('feedback/', FeedbackView.as_view(), name='give-feedback'),
    # path('login/', auth_views.LoginView.as_view(template_name='store/login_user.html'), name='login-user'),
    path('login/', loginPage, name='login-user'),
    path('home/', HomeView.as_view(), name="grocery_store_home"),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout-user'),
    path('admin/', admin.site.urls, name='admin:index'),
    path('profile/', profile, name='user-profile'),

]