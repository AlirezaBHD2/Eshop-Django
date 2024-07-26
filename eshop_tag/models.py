# Import the necessary module from Django
from django.db import models
from django.db.models.signals import pre_save
from eshop_product.models import Product
from .utils import unique_slug_generator


# Define the Tag model
class Tag(models.Model):
    # The title of the tag, e.g., "New Arrival", "On Sale"
    title = models.CharField(
        max_length=120,
        verbose_name='عنوان'
    )

    # Slug field for URL-friendly representation of the title
    slug = models.SlugField(
        verbose_name='عنوان در url'
    )

    # Timestamp field to automatically record the date and time when the tag is created
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )

    # Boolean field to indicate if the tag is active or not
    active = models.BooleanField(
        default=True,
        verbose_name='فعال / غیر فعال'
    )

    # Many-to-Many relationship with Product model; a tag can be associated with multiple products
    products = models.ManyToManyField(
        Product,
        blank=True,
        verbose_name='محصولات'
    )

    def __str__(self):
        # Return the title of the tag when the instance is converted to a string
        return self.title

    class Meta:
        # Define the verbose names for the model in the Django admin interface
        verbose_name = 'برچسب / تگ'
        verbose_name_plural = 'برچسب ها / تگ ها'


# Function to handle the pre-save signal for the Tag model
def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    # Check if the slug is not set
    if not instance.slug:
        # Generate a unique slug using the utility function
        instance.slug = unique_slug_generator(instance)


# Connect the tag_pre_save_receiver function to the pre_save signal of the Tag model
pre_save.connect(tag_pre_save_receiver, sender=Tag)
