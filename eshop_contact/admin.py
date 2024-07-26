from django.contrib import admin
from eshop_contact.models import ContactUs, EmailNews


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['subject', 'full_name', 'is_read']
    list_filter = ["is_read"]
    list_editable = ["is_read"]
    search_fields = ["subject", "full_name", "text"]

    class Meta:
        model = ContactUs


class EmailNewsAdmin(admin.ModelAdmin):
    class Meta:
        model = EmailNews


admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(EmailNews, EmailNewsAdmin)
