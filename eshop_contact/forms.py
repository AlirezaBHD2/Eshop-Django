# Import necessary modules from Django
from django import forms
from django.core import validators
from django.contrib.auth.models import User

# Define the form for creating a contact message
class CreateContactForm(forms.Form):
    # Define the full name field with a text input widget, placeholder, and class
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'لطفا نام و نام خوانوادگی خود را وارد نمایید', 'class': 'form-control'}),
        label='نام و نام خوانوادگی',
        validators=[validators.MaxLengthValidator(150, "نام و نام خوانوادگی شما نمیتواند بیشتر از 150 باشد")]
    )

    # Define the email field with an email input widget, placeholder, and class
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید', 'class': 'form-control'}),
        label='ایمیل',
        validators=[validators.MaxLengthValidator(150, "ایمیل شما نمیتواند بیشتر از 150 کاراکتر باشد")]
    )

    # Define the subject field with a text input widget, placeholder, and class
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا عنوان پیام خود را وارد نمایید', 'class': 'form-control'}),
        label='عنوان',
        validators=[validators.MaxLengthValidator(150, "عنوان پیام شما نمیتواند بیشتر از 150 کاراکتر باشد")]
    )

    # Define the text field with a textarea widget, placeholder, class, and rows
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'لطفا متن پیام خود را وارد نمایید', 'class': 'form-control', 'rows': '8'}),
        label='پیام',
    )

# Define the form for subscribing to emails
class CreateEmailForm(forms.Form):
    # Define the email field with an email input widget, placeholder, and class
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید', 'class': 'form-control'}),
        label='ایمیل',
        validators=[validators.MaxLengthValidator(150, "ایمیل شما نمیتواند بیشتر از 150 کاراکتر باشد")]
    )
