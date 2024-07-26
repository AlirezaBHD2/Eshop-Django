from django.urls import path
from .views import add_wish_list , remove_wish_list

urlpatterns = [
    path('wishlist/add/<productId>', add_wish_list),
    path('wishlist/remove/<productId>', remove_wish_list),
]
