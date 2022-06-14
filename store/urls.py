from . views import HomeView, register, registerbrand, FeedbackView, change_password, AboutView, loginPage, profile
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('', HomeView.as_view(), name="grocery_store_home"),
    # path('home/', HomeView.as_view(), name='grocery_store_home'),
    path('register/', register, name='register-user'),
    path('brand-register/', registerbrand, name="register-brand"),
    path('about/', AboutView.as_view(), name='about-us'),
    path('feedback/', FeedbackView.as_view(), name='give-feedback'),
    # path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login-user'),
    path('login/', loginPage, name='login'),
    path('home/', HomeView.as_view(), name="grocery_store_home"),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout-user'),
    path('admin/', admin.site.urls, name='admin:index'),
    path('profile/', profile, name='user-profile'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='store/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='store/password_reset_complete.html'),
         name='password_reset_complete'),
    path('change=password', change_password, name='change_password'),

]