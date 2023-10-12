from urllib import request
from django.contrib.auth import authenticate
from django import forms
from .models import User, Otp, UserAddress, Profile, ContactUs
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'email', 'password', 'image_profile', 'is_active', 'is_admin')


class AddressCreationForm(forms.ModelForm):
    user = forms.IntegerField(required=False)

    class Meta:
        model = UserAddress
        fields = '__all__'
        widgets = {
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username or Phone"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))

    def clean_password(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user is not None:
            return self.cleaned_data.get('password')
        raise ValidationError('your username or password is invalid')


class OtpLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
                            validators=[validators.MaxLengthValidator(90), validators.MinLengthValidator(11)])
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
                                validators=[validators.MinLengthValidator(6)])
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Repeat password"}),
        validators=[validators.MinLengthValidator(6)])

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data.get('username')):
            raise ValidationError('This username before exist')
        return self.cleaned_data.get('username')

    def clean_password1(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise ValidationError('Your password is not the same')
        return self.cleaned_data.get('password1')



class CheckOtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Code"}),
                           validators=[validators.MaxLengthValidator(4)])


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email']
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data.get("username")).exists():
            raise ValidationError("This username before exists", code="username_exists")
        return self.cleaned_data.get("username")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={"class": "form-control btn btn-info", 'value': 'select'}),
        }

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'message'})
        }