# import random
# import string
# from django.utils.text import slugify
#
# def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))
#
#
# print(random_string_generator())
#
# print(random_string_generator(size=50))
#
#
# def unique_slug_generator(instance, new_slug=None):
#     """
#     This is for a Django project and it assumes your instance
#     has a model with a slug field and a title character (char) field.
#     """
#     if new_slug is not None:
#         slug = new_slug
#     else:
#         slug = slugify(instance.title)
#
#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(
#             slug=slug,
#             randstr=random_string_generator(size=4)
#         )
#         return unique_slug_generator(instance, new_slug=new_slug)
#     return slug

import random
import string
from django.utils.text import slugify


# Function to generate a random string of a specified size
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Test the random string generator with default size
print(random_string_generator())

# Test the random string generator with a size of 50
print(random_string_generator(size=50))


# Function to generate a unique slug for a given instance
def unique_slug_generator(instance, new_slug=None):
    """
    This function generates a unique slug for a Django model instance.

    Assumptions:
    - The instance has a model with a 'slug' field and a 'title' character (char) field.
    - If a new_slug is provided, it uses that; otherwise, it generates a slug from the title.
    """

    # If a new slug is provided, use it; otherwise, create a slug from the title
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    # Get the class of the instance to query the database
    Klass = instance.__class__

    # Check if a slug with the same name already exists in the database
    qs_exists = Klass.objects.filter(slug=slug).exists()

    # If the slug exists, append a random string to make it unique
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)

    # Return the unique slug
    return slug
