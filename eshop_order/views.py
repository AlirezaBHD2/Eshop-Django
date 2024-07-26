# Import the necessary module from Django
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from eshop_product.models import Product
from .forms import UserNewOrderForm
from .models import Order, OrderDetail
from django.http import HttpResponse, Http404
from zeep import Client


# A decorator to ensure that the user is authenticated before accessing the view.
# If not authenticated, it redirects the user to the login page.
@login_required(login_url="/login")
def add_user_order_single(request, *args, **kwargs):
    # Check if an unpaid order exists for the user, otherwise create one.
    order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    if order is None:
        order = Order.objects.create(owner_id=request.user.id, is_paid=False)

    # Get the product ID and create a new order detail.
    product_id = kwargs['productId']
    count = 1
    product = Product.objects.get_by_id(product_id)

    # Check if the product is already in the order, update the count of the existing order detail.
    same_order = OrderDetail.objects.filter(order=order.id, product=Product.objects.filter(id=product_id).first())
    same_order_count = len(
        OrderDetail.objects.filter(order=order.id, product=Product.objects.filter(id=product_id).first()))
    if same_order_count == 1:
        same_order.update(count=str(count + int(same_order.first().count)))
    else:
        order.orderdetail_set.create(product_id=product.id, price=product.price, count=count)

    # Redirect to the previous page.
    return redirect(request.META.get('HTTP_REFERER'))


# A view for deleting an order detail.
@login_required(login_url="/login")
def delete_order_detail(request, *args, **kwargs):
    detail_id = kwargs.get("detail_id")
    if detail_id is not None:
        # Get the order detail by id and check if it belongs to the user, then delete it.
        order_detail = OrderDetail.objects.filter(id=detail_id, order__owner_id=request.user.id)
        if order_detail is not None:
            order_detail.delete()

    # Redirect to the open-order page.
    return redirect("/open-order")


# Only authenticated users can access this function
@login_required(login_url="/login")
def add_user_order(request):
    # Create a form instance from the submitted data
    new_order_form = UserNewOrderForm(request.POST or None)
    # Get the first product from the database
    product = Product.objects.first()
    # If the form is valid, process the data
    if new_order_form.is_valid():
        # Get the current order for the user if it exists, otherwise create a new one
        order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if order is None:
            order = Order.objects.create(owner_id=request.user.id, is_paid=False)
        # Get the product ID and count from the form data
        product_id = new_order_form.cleaned_data.get("product_id")
        count = new_order_form.cleaned_data.get("count")
        # Ensure that the count is not negative
        if count < 0:
            count = 1
        # Get the product instance with the specified ID
        product = Product.objects.get_by_id(product_id)
        # Get any existing order details for the specified product and order
        same_order = OrderDetail.objects.filter(order=order.id, product=Product.objects.filter(id=product_id).first())
        same_order_count = len(
            OrderDetail.objects.filter(order=order.id, product=Product.objects.filter(id=product_id).first()))
        # If there is an existing order detail, update its count with the new count
        if same_order_count == 1:
            # print(count)
            print(same_order.first().count)
            same_order.update(count=str(count + int(same_order.first().count)))
        # Otherwise, create a new order detail for the product
        else:
            order.orderdetail_set.create(product_id=product.id, price=product.price, count=count)

    # Redirect the user to the product page
    return redirect(f"/products/{product.id}/{product.title}")


# Only authenticated users can access this function
@login_required(login_url="/login")
def user_open_order(request):
    # Initialize the context dictionary
    context = {"order": None,
               "details": None,
               "total": 0,
               "taxation": 0,
               "F_total": 0}
    # Get the current open order for the user if it exists
    open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    # If there is an open order, populate the context dictionary with its details
    if open_order is not None:
        context["order"] = open_order
        context["details"] = open_order.orderdetail_set.all()
        context["total"] = open_order.get_total_price()
        context["taxation"] = context["total"] * 0.09
        context["F_total"] = context["total"] + context["taxation"]
    # Render the order page with the context dictionary
    return render(request, "order/user_open_order.html", context)


# Initialize the ZarinPal client with the service WSDL URL
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# Set the merchant ID for ZarinPal transactions
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# Set the description for the transaction (required)
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
# Set the email and mobile number for the transaction (optional)
email = 'email@example.com'
# Set the mobile number for the transaction (optional)
mobile = '09123456789'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://localhost:8000/verify'  # Important: need to edit for really server.


# This function sends a payment request to a payment gateway and redirects the user to the payment gateway's page
def send_request(request, *args, **kwargs):
    total_price = 0
    # Get the first unpaid order for the current user
    open_order: Order = Order.objects.filter(is_paid=False, owner_id=request.user.id).first()
    # If an unpaid order exists, get its total price and send a payment request to the payment gateway
    if open_order is not None:
        total_price = open_order.get_total_price()
        result = client.service.PaymentRequest(
            MERCHANT, total_price, description, email, mobile, f"{CallbackURL}/{open_order.id}")
        # If the payment request is successful, redirect the user to the payment gateway's page
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        # If the payment request fails, return an error message
        else:
            return HttpResponse('Error code: ' + str(result.Status))
    # If no unpaid order exists, raise a 404 error
    raise Http404()


# This function verifies a payment made through the payment gateway and updates the order accordingly
def verify(request, **kwargs):
    order_id = kwargs.get("order_id")
    # If the payment was successful
    if request.GET.get('Status') == 'OK':
        # Verify the payment with the payment gateway
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'])
        # If the payment verification is successful, update the order to mark it as paid
        if result.Status == 100:
            user_order = Order.objects.get_queryset().get(id=order_id)
            user_order.is_paid = True
            user_order.payment_date = time.time()
            user_order.refID = result.RefID
            user_order.save()
            # Return a success message with the reference ID of the payment
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        # If the payment is still being processed, return a message indicating this
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        # If the payment verification fails, return an error message
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    # If the payment was not successful, return an error message
    else:
        return HttpResponse('Transaction failed or canceled by user')
