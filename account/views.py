from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Otp, Profile, ContactUs
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import AddressCreationForm, LoginForm, OtpLoginForm, CheckOtpForm, UserUpdateForm, ProfileUpdateForm, \
    ContactUsForm
from django.contrib import messages
import ghasedakpack
from random import randint
from uuid import uuid4

SMS = ghasedakpack.Ghasedak("16e061d580d3128b17f425aee0a4be090e5e7bfc11e3a02c9c80f1d6c5961e65")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'account/Login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return form.add_error('username', 'invalid data')
        return render(request, 'account/Login.html', {'form': form})


class OtpRegisterView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = OtpLoginForm()
            return render(request, "account/Register.html", {"form": form})
        return redirect('/')

    def post(self, request):
        form = OtpLoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            SMS.verification({'receptor': cd["phone"], 'type': '1', 'template': 'code', 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd["phone"], username=cd['username'], password1=cd['password1'],
                               code=randcode, token=token)
            print(randcode)
            return redirect(reverse("check_opt") + f"?token={token}")

        return render(request, "account/Register.html", {"form": form})


class CheckOtpView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = CheckOtpForm()
            return render(request, "account/check_otp.html", {"form": form})
        return redirect('/')

    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd["code"], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_created = User.objects.get_or_create(phone=otp.phone, username=otp.username)
                user.set_password(otp.password1)
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect("product:home")
            else:
                form.add_error("code", "This code is not valid")

        return render(request, "account/check_otp.html", {"form": form})

class RestPasswordView(View):
    def get(self, request):
        pass


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
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            return redirect('account:profile_update')  # Redirect back to profile page
        elif p_form.is_valid():
            p_form.save()

            return redirect('account:profile_update')
        elif u_form.is_valid():
            u_form.save()

            return redirect('account:profile_update')

        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_form': u_form,
            'profile_form': p_form
        }
        return render(request, 'account/profile.html', context)


class ContactUsView(View):
    success_message = 'send'
    def get(self, request):
        form = ContactUsForm()
        return render(request, 'account/contact.html', {'form': form})
    def post(self, request):
        form = ContactUsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ContactUs.objects.create(name=cd.get("name"), email=cd.get('email'), subject=cd.get('subject'), message=cd.get('message'))
            messages.add_message(request, messages.SUCCESS, 'Your message has been sent')
            form = ContactUsForm()
            return render(request, 'account/contact.html', {'form': form})


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("/")
