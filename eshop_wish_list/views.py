# Import the necessary module from Django
from django.shortcuts import render, redirect
from .models import Wish_List
from eshop_product.models import Product
from django.http import HttpResponse


def add_wish_list(request, *args, **kwargs):
    # Get the user ID and the product ID from the URL
    user = request.user.id
    product_id = kwargs['productId']

    # If the user doesn't have a wish list, create one
    if Wish_List.objects.filter(user=user).first() == None:
        Wish_List.objects.create(user=user)

    # Add the selected product to the user's wish list
    Wish_List.objects.filter(user=user)[0].products.add(Product.objects.get(id=product_id))

    # Redirect the user to the previous page
    return redirect(request.META.get('HTTP_REFERER'))


def remove_wish_list(request, *args, **kwargs):
    # Get the user ID and the product ID from the URL
    user = request.user.id
    product_id = kwargs['productId']

    # If the user has a wish list, remove the selected product from it
    if Wish_List.objects.filter(user=user).first() != None:
        Wish_List.objects.filter(user=user)[0].products.remove(Product.objects.get(id=product_id))

    # Redirect the user to the previous page
    return redirect(request.META.get('HTTP_REFERER'))
