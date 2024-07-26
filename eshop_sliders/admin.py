from django.contrib import admin
from .models import Slider
# Register your models here.


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title']

    class Meta:
        model = Slider


admin.site.register(Slider, SliderAdmin)