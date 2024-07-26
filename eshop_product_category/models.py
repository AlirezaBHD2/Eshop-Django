from django.db import models


# Define the ProductCategory model
class ProductCategory(models.Model):
    # Title field for the category, e.g., "Electronics", "Clothing"
    title = models.CharField(
        max_length=150,
        verbose_name='عنوان'
    )

    # Name field for the category used in URLs, e.g., "electronics", "clothing"
    name = models.CharField(
        max_length=150,
        verbose_name='عنوان در URL'
    )

    class Meta:
        # Specify the singular and plural names for the model in the admin interface
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        # Return the title of the category as the string representation
        return self.title
