from django.urls import path
from eshop_order.views import add_user_order, user_open_order,add_user_order_single, send_request, verify , delete_order_detail

urlpatterns = [
    path('add_user_order', add_user_order),
    path('add_user_order/<productId>', add_user_order_single),
    path('open-order', user_open_order),
    path('delete_order_detail/<detail_id>', delete_order_detail),
    path('request', send_request, name='request'),
    path('verify/<order_id>', verify, name='verify'),
]
