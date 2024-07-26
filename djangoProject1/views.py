# Import the necessary module from Django
import itertools
from django.views.generic import ListView
from django.http import Http404
from django.shortcuts import render, redirect
from eshop_product.models import Product
from eshop_product_category.models import ProductCategory
from eshop_sliders.models import Slider
from eshop_settings.models import SiteSetting
from eshop_wish_list.models import Wish_List
from eshop_contact.forms import CreateEmailForm
from eshop_contact.models import EmailNews


# Header code behind
def header(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()
    context = {
        'setting': site_setting
    }
    return render(request, 'shared/Header.html', context)


# Footer code behind
def footer(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()

    # Handle the contact form for sending news to customers
    # Create an instance of the form, validate it, and save the email to the database if it is not already present
    contact_form = CreateEmailForm(request.POST or None)
    if contact_form.is_valid():
        email = contact_form.cleaned_data.get("email")
        if email not in EmailNews.objects.all():
            EmailNews.objects.create(email=email)

    context = {
        'setting': site_setting,
        'contact_form': contact_form
    }
    return render(request, 'shared/Footer.html', context)


# Home page code behind
def home_page(request):
    categories = ProductCategory.objects.all()
    sliders = Slider.objects.all()

    # Retrieve the most visited and latest products
    most_visit_products = Product.objects.order_by("-visit_count").all()[:8]
    latest = Product.objects.order_by("-id").all()[:8]

    products_by_category = []

    # Iterate over each category, retrieve products belonging to that category, and group them into lists of 4
    for category in categories:
        products = Product.objects.all()
        same_category = []
        for product in products:
            # Only add the product to the category list if it belongs to the current category and the list does not already contain 4 products
            if len(same_category) != 4 and product.categories.first() == category:
                same_category.append(product)
        products_by_category.append(same_category)

    # Retrieve the user's wish list, if it exists
    wish_list = []
    if Wish_List.objects.filter(user=request.user.id).first():
        wish_list = Wish_List.objects.filter(user=request.user.id).first().products.all()

    # Populate the context dictionary with data for the template
    context = {
        "Sliders": sliders,
        "most_visited": list(most_visit_products),
        "latest_products": list(latest),
        'categories': categories,
        "products_by_category": products_by_category,
        "wish_list": wish_list
    }

    return render(request, 'home_page.html', context)


# About page code behind
def about_page(request):
    site_setting = SiteSetting.objects.first()
    context = {'setting': site_setting}
    return render(request, "about_page.html", context)


# A class-based view for displaying products by category
class ProductsListByCategory(ListView):
    def get_queryset(self):
        # Get the category name from the URL parameters
        category_name = self.kwargs['category_name']
        # Find the category object that matches the name
        category = ProductCategory.objects.filter(name__iexact=category_name).first()
        # Raise a 404 error if the category isn't found
        if category is None:
            raise Http404('صفحه ی مورد نظر یافت نشد')
        # Return the products that belong to the category
        return Product.objects.get_products_by_category(category_name)


# A view for submitting an email form
def get_email(request):
    # Create a form instance with POST data or None if the form has not been submitted
    contact_form = CreateContactForm(request.POST or None)
    if contact_form.is_valid():
        # If the form is valid, extract the email from the cleaned data
        email = contact_form.cleaned_data.get("email")
    # Redirect the user back to the previous page
    return redirect(request.META.get('HTTP_REFERER'))
