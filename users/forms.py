from django import forms
from django.contrib.auth.models import User
from . models import Customer


class FormUser(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username",
        "required": "required",
    }))
    last_name = forms.CharField(max_length=264, label="Họ", widget=forms.TextInput(attrs={
        'id': 'last_name',
        'class': 'form-control',
        'placeholder': 'Họ',
        'required': 'required'
    }))
    first_name = forms.CharField(max_length=264, label="Tên", widget=forms.TextInput(attrs={
        'id': 'first_name',
        'class': 'form-control',
        'placeholder': 'Tên',
        'required': 'required'
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'id': 'email',
        'class': 'form-control',
        'placeholder': 'Địa chỉ Email',
        'required': 'required'
    }))
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput(attrs={
        'id': 'password',
        'class': 'form-control',
        'placeholder': 'Mật khẩu',
        'required': 'required'
    }))
    confirm_password = forms.CharField(label="Xác nhận mật khẩu", widget=forms.PasswordInput(attrs={
        'id': 'confirm_password',
        'class': 'form-control',
        'placeholder': 'Xác nhận mật khẩu',
        'required': 'required'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class FormCustomer(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, label="Điện thoại", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Điện thoại',
        'required': 'required'
    }))
    address = forms.CharField(label="Địa chỉ", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Địa chỉ',
        'required': 'required'
    }))

    class Meta:
        model = Customer
        exclude = ('user',)