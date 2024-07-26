# Import the necessary module from Django
from django.db import models


# Define the ContactUs model to store contact messages
class ContactUs(models.Model):
    # Define the full name field with a maximum length of 200 characters
    full_name = models.CharField(null=True, max_length=200, verbose_name="نام و نام خانوادگی")

    # Define the email field with a maximum length of 150 characters
    email = models.EmailField(null=True, max_length=150, verbose_name="ایمیل")

    # Define the subject field with a maximum length of 210 characters
    subject = models.CharField(null=True, max_length=210, verbose_name="عنوان پیام")

    # Define the text field to store the message content
    text = models.TextField(null=True, verbose_name="متن پیام")

    # Define the is_read field to indicate if the message has been read
    is_read = models.BooleanField(null=True, verbose_name="خوانده شده")

    # Meta options for the ContactUs model
    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'تماس های کاربران'

    # String representation of the model, returning the subject of the message
    def __str__(self):
        return self.subject


# Define the EmailNews model to store email subscriptions
class EmailNews(models.Model):
    # Define the email field with a maximum length of 150 characters
    email = models.EmailField(null=True, max_length=150, verbose_name="ایمیل")

    # Meta options for the EmailNews model
    class Meta:
        verbose_name = 'ایمیل کاربران'
        verbose_name_plural = 'ایمیل کاربران'

    # String representation of the model, returning the email address
    def __str__(self):
        return self.email
