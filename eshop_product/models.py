# Import necessary modules from Django
from django.db.models import Q
from django.db import models
import os

# Import the ProductCategory model from the eshop_product_category app
from eshop_product_category.models import ProductCategory

# Function to get the filename and extension of a file
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

# Function to determine the upload path for product images
def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/{final_name}"

# Function to determine the upload path for gallery images
def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/galleries/{final_name}"

# Manager class for the Product model with custom query methods
class ProductsManager(models.Manager):
    # Method to get active products
    def get_active_products(self):
        return self.get_queryset().filter(active=True)

    # Method to order products based on a given order
    def get_by_order(self, given_order):
        return self.get_queryset().order_by(given_order)

    # Method to get products by category name
    def get_products_by_category(self, category_name):
        return self.get_queryset().filter(categories__name__iexact=category_name, active=True)

    # Method to get a product by its ID
    def get_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    # Method to search products by a query string
    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__title__icontains=query)
        )
        return self.get_queryset().filter(lookup, active=True).distinct()

# Define the Product model
class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تصویر')
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    categories = models.ManyToManyField(ProductCategory, blank=True, verbose_name="دسته بندی ها")
    existing = models.BooleanField(default=True, verbose_name="موجود")
    visit_count = models.IntegerField(default=0, verbose_name="تعداد بازدید")

    # Use the custom manager
    objects = ProductsManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    # String representation of the product
    def __str__(self):
        return self.title

    # Method to get the absolute URL of the product
    def get_absolute_url(self):
        return f"/products/{self.id}/{self.title.replace(' ', '-')}"


# Define the ProductGallery model
class ProductGallery(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان")
    image = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

    # String representation of the gallery image
    def __str__(self):
        return self.title
