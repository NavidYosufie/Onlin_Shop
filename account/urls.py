from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="user_login"),
    path("register", views.OtpRegisterView.as_view(), name="user_register"),
    path("checkotp", views.CheckOtpView.as_view(), name="check_opt"),
    path("add/address", views.AddAddressView.as_view(), name="add_address"),
    path("profile", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("logout", views.UserLogout.as_view(), name="user_logout"),
]