# Import necessary modules from Django
from django import forms
from django.contrib.auth.models import User
from django.core import validators

# Define the form for creating a new order by a user
class UserNewOrderForm(forms.Form):
    # Define the product_id field as an integer field with a hidden input widget
    product_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    # Define the count field as an integer field with a number input widget and an initial value of 1
    count = forms.IntegerField(
        widget=forms.NumberInput(),
        initial=1
    )
