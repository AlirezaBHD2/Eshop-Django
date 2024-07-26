# Import necessary modules from Django
from django.db import models
from django.contrib.auth.models import User

# Import the Product model from the product app
from eshop_product.models import Product


# Define the Order model to represent a user's order
class Order(models.Model):
    # Define a foreign key to the User model, with cascading deletion and null value allowed
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # Define a boolean field to indicate if the order is paid
    is_paid = models.BooleanField(null=True, verbose_name="پرداخت شده")

    # Define an integer field for the payment reference ID
    refID = models.IntegerField(null=True, verbose_name="کد پیگیری")

    # Define a DateTimeField for the payment date, allowing blank and null values
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ پرداخت")

    # Meta options for the Order model
    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید کاربران"

    # String representation of the model, returning the order ID as a string
    def __str__(self):
        return str(self.id)

    # Method to calculate the total price of the order
    def get_total_price(self):
        amount = 0
        # Iterate over all related OrderDetail objects and sum their total prices
        for detail in self.orderdetail_set.all():
            amount += detail.price * detail.count
        return amount


# Define the OrderDetail model to represent details of products in an order
class OrderDetail(models.Model):
    # Define a foreign key to the Order model, with cascading deletion
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    # Define a foreign key to the Product model
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")

    # Define an integer field for the product's price
    price = models.IntegerField(verbose_name="قیمت محصول")

    # Define an integer field for the quantity of the product
    count = models.IntegerField(verbose_name="تعداد")

    # Method to calculate the sum of the product's price for the quantity ordered
    def get_detail_sum(self):
        return self.count * self.price

    # Meta options for the OrderDetail model
    class Meta:
        verbose_name = "جزئیات محصول"
        verbose_name_plural = "اطلاعات جزئیات محصولات"

    # String representation of the model, returning the product title
    def __str__(self):
        return self.product.title
