from django import forms
from django.contrib.auth.models import User
from django.core import validators

# Define the form for editing user information
class EditUserForm(forms.Form):
    # Define the first name field with a text input widget and a placeholder
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'لطفا نام خود را وارد نمایید'}),
        label='نام'
    )

    # Define the last name field with a text input widget and a placeholder
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'لطفا نام خوانوادگی خود را وارد نمایید'}),
        label='نام خوانوادگی'
    )

# Define the form for user login
class LoginForm(forms.Form):
    # Define the username field with a text input widget and a placeholder
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'لطفا نام کاربری خود را وارد نمایید'}),
        label='نام کاربری'
    )

    # Define the password field with a password input widget and a placeholder
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید'}),
        label='کلمه ی عبور'
    )

    # Custom validator for the username field
    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user = User.objects.filter(username=user_name).exists()
        if not is_exists_user:
            raise forms.ValidationError('کاربری با مشخصات وارد شده ثبت نام نکرده است')
        return user_name

# Define the form for user registration
class RegisterForm(forms.Form):
    # Define the username field with validation for length
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری خود را وارد نمایید'}),
        label='نام کاربری',
        validators=[
            validators.MaxLengthValidator(limit_value=20, message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(8, 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    # Define the email field with validation for format and length
    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید'}),
        label='ایمیل',
        validators=[
            validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    # Define the password field with a password input widget and a placeholder
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید'}),
        label='کلمه ی عبور'
    )

    # Define the re-password field with a password input widget and a placeholder
    re_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا تکرار کلمه عبور خود را وارد نمایید'}),
        label='تکرار کلمه ی عبور'
    )

    # Custom validator for the email field
    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_user_by_email = User.objects.filter(email=email).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')

        if len(email) > 320:
            raise forms.ValidationError('تعداد کاراکترهای ایمیل باید کمتر از 320 باشد')

        return email

    # Custom validator for the username field
    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user_by_username = User.objects.filter(username=user_name).exists()
        if is_exists_user_by_username:
            raise forms.ValidationError('این کاربر قبلا ثبت نام کرده است')
        return user_name

    # Custom validator for the re-password field to check if passwords match
    def clean_re_password(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')
        return password
