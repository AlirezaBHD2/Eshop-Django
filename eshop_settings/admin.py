from django.contrib import admin
from .models import SiteSetting, SocialMedia

# Register your models here.

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['social_name']

    class Meta:
        model = SocialMedia


admin.site.register(SiteSetting)
admin.site.register(SocialMedia , SocialMediaAdmin)
