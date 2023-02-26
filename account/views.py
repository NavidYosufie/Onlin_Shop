from msilib.schema import ListView

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Otp, Profile
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import AddressCreationForm, LoginForm, OtpLoginForm, CheckOtpForm, UserUpdateForm, ProfileUpdateForm
import ghasedakpack
from random import randint
from uuid import uuid4
from django.views.generic import UpdateView, CreateView, FormView

SMS = ghasedakpack.Ghasedak("16e061d580d3128b17f425aee0a4be090e5e7bfc11e3a02c9c80f1d6c5961e65")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account/Login.html", {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                return redirect("home:home")
            else:
                form.add_error("phone", "Your username or password is incorrect")

        return render(request, 'account/Login.html', {"form": form})


class OtpLoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, "account/Register.html", {"form": form})

    def post(self, request):
        form = OtpLoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            template = f"for register to site code:{randcode}"
            SMS.verification({'receptor': cd["phone"], 'type': '1', 'template': template, 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd["phone"], code=randcode, token=token)
            print(randcode)

            return redirect(reverse("account:check_opt") + f"?token={token}")

        return render(request, "account/Register.html", {"form": form})


class CheckOtpView(View):

    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account/check_otp.html", {"form": form})

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd["code"], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect("product:home")

            else:
                form.add_error("code", "This code is not valid")

        return render(request, "account/check_otp.html", {"form": form})


class AddAddressView(View):
    def get(self, request):
        form = AddressCreationForm()
        return render(request, "account/add_address.html", {"form": form})

    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get("next")
            if next_page:
                return redirect(next_page)
            return render(request, "account/add_address.html", {"form": form})
        else:
            form.add_error("phone", 'this errors')


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'account/profile.html', {'user_form': u_form, 'profile_form': p_form})

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() or p_form.is_valid():
            u_form.save()
            p_form.save()

            return redirect('account:profile_update') # Redirect back to profile page
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_form': u_form,
            'profile_form': p_form
        }
        return render(request, 'account/profile.html', context)


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("/")
