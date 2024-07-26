# Import the necessary module from Django
from django.db import models
from eshop_product.models import Product


# Create your models here.
class Wish_List(models.Model):
    # The user who owns this wish list
    user = models.CharField(max_length=200, verbose_name='کاربر')

    # Products that are added to the user's wish list
    products = models.ManyToManyField(Product, blank=True, verbose_name='محصولات')

    class Meta:
        # Singular name for the model in the admin interface
        verbose_name = 'لیست علاقه مندی ها'

        # Plural name for the model in the admin interface
        verbose_name_plural = 'لیست علاقه مندی ها'
