from django.contrib import admin

# Register your models here.
from eshop_order.models import Order, OrderDetail


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'owner']

    class Meta:
        model = Order
admin.site.register(Order , OrderAdmin)
admin.site.register(OrderDetail)
