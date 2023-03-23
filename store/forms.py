from django import forms
from . models import Contact


class FormContact(forms.ModelForm):
    last_name = forms.CharField(max_length=150, label="Last Name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Họ',
        'required': 'required'
    }))
    first_name = forms.CharField(max_length=150, label="Name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Tên',
        'required': 'required'
    }))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Địa chỉ Email',
        'required': 'required'
    }))
    phone_number = forms.CharField(max_length=20, label="Phone Number", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Số điện thoại',
        'required': 'required'
    }))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Nội dung',
        'rows': '5',
        'required': 'required'
    }))

    class Meta:
        model = Contact
        fields = '__all__' #('name', 'email',)