from django.contrib import admin
from .models import Wish_List

class WishListAdmin(admin.ModelAdmin):
    list_display = ['user','__str__']

    class Meta:
        model = Wish_List


admin.site.register(Wish_List, WishListAdmin)
