from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

#app_name = "account"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="user_login"),
    path("register", views.OtpRegisterView.as_view(), name="user_register"),
    path("checkotp", views.CheckOtpView.as_view(), name="check_opt"),
    path("add/address", views.AddAddressView.as_view(), name="add_address"),
    path("contactus", views.ContactUsView.as_view(), name="contactus"),
    path("profile", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("password_change", auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html'), name="password_change"),
    path('password_chanhe/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    path('password_rest', views.RestPasswordView.as_view(), name='password_rest'),
    path('otp_password_rest', views.OtpRestPasswordView.as_view(), name='otp_rest_password'),
    path("logout", views.UserLogout.as_view(), name="user_logout"),
]