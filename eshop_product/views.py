# Import the necessary module from Django
import itertools
import datetime
from django.shortcuts import render
from django.views.generic import ListView
from eshop_order.forms import UserNewOrderForm
from .models import Product, ProductGallery
from django.http import Http404
from eshop_product_category.models import ProductCategory
from eshop_settings.models import SocialMedia


# A function to group items in an iterable into tuples of a specific size.
def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))



# A view to display a list of active products, using a template
# that shows them in a grid with pagination.
class ProductsList(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    # Get the queryset of active products to display.
    def get_queryset(self):
        return Product.objects.get_active_products()


# A view to display a list of products in a specific order,
# using a template that shows them in a grid with pagination.
class ProductsListByOrder(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    # Get the queryset of products in the specified order to display.
    def get_queryset(self):
        return Product.objects.get_by_order(self.kwargs['order'])


# A view to display a list of products in a specific category,
# using a template that shows them in a grid with pagination.
class ProductsListByCategory(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    # Get the queryset of products in the specified category to display.
    def get_queryset(self):
        category_name = self.kwargs['category_name']
        category = ProductCategory.objects.filter(name__iexact=category_name).first()
        if category is None:
            raise Http404('صفحه ی مورد نظر یافت نشد')
        return Product.objects.get_products_by_category(category_name)


def product_detail(request, *args, **kwargs):
    # Get the selected product ID from URL parameters
    selected_product_id = kwargs['productId']
    # Create a new order form instance with the selected product ID
    new_order_form = UserNewOrderForm(request.POST or None, initial={"product_id": selected_product_id})
    # Retrieve the product object from the database using the selected product ID
    product: Product = Product.objects.get_by_id(selected_product_id)
    # Retrieve all social media links from the database
    social_media = SocialMedia.objects.all()

    # Raise a 404 error if the product is not found or inactive
    if product is None or not product.active:
        raise Http404('محصول مورد نظر یافت نشد')

    # Increase the product visit count by 1 and save it
    product.visit_count += 1
    product.save()

    # Retrieve all related products of the selected product
    related_products = Product.objects.get_queryset().filter(categories__product=product).distinct()

    # Group the related products in groups of 3
    grouped_related_products = my_grouper(3, related_products)

    # Create a context dictionary to pass data to the template
    context = {
        'product': product,
        'related_products': grouped_related_products,
        "new_order_form": new_order_form,
        "date": datetime.datetime.now().date,
        "social_media": social_media
    }

    # Render the product detail template with the context data
    return render(request, 'products/product_detail.html', context)


class SearchProductsView(ListView):
    template_name = 'products/products_list.html'
    paginate_by = 6

    def get_queryset(self):
        # Get the query parameter from the URL
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            # Return the search results for the query
            return Product.objects.search(query)

        # Return all active products if there is no query parameter
        return Product.objects.get_active_products()


def products_categories_partial(request):
    # Retrieve all product categories from the database
    categories = ProductCategory.objects.all()
    # Create a context dictionary to pass data to the template
    context = {
        'categories': categories
    }
    # Render the product categories partial template with the context data
    return render(request, 'products/products_categories_partial.html', context)
