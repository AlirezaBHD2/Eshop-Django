# Import the necessary module from Django
import os
from django.db import models


# Function to extract the filename and extension from a given file path
def get_filename_ext(filepath):
    # Extract the base name of the file from the file path (e.g., 'image.png' from '/path/to/image.png')
    base_name = os.path.basename(filepath)
    # Split the base name into name and extension (e.g., 'image' and '.png')
    name, ext = os.path.splitext(base_name)
    return name, ext


# Function to generate the upload path for slider images
def upload_image_path(instance, filename):
    # Get the name and extension of the uploaded file
    name, ext = get_filename_ext(filename)
    # Construct the final name for the file using the instance ID and title
    final_name = f"{instance.id}-{instance.title}{ext}"
    # Define the upload path for the file under the 'sliders/' directory
    return f"sliders/{final_name}"


# Model for slider images
class Slider(models.Model):
    # Title of the slider, e.g., "Summer Sale", "New Arrivals"
    title = models.CharField(
        max_length=150,
        verbose_name="عنوان"
    )

    # URL that the slider should link to when clicked
    link = models.URLField(
        max_length=100,
        verbose_name="آدرس"
    )

    # Description of the slider, which may include details about the offer or promotion
    description = models.TextField(
        verbose_name="توضیحات"
    )

    # Image associated with the slider; the image file will be uploaded to the path specified by 'upload_image_path'
    image = models.ImageField(
        upload_to=upload_image_path,
        null=True,
        blank=True,
        verbose_name='تصویر'
    )

    class Meta:
        # Define the singular and plural names for the model in the Django admin interface
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'

    def __str__(self):
        # Return the title of the slider as the string representation
        return self.title
