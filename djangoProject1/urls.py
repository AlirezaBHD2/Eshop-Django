from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import home_page, get_email
from djangoProject1.views import header, footer, about_page
from django.conf import settings

# from e_shop import settings

urlpatterns = [
    path('', home_page),
    path('admin/', admin.site.urls),
    path('header', header, name="header"),
    path('footer', footer, name="footer"),
    path('about-us', about_page),
    path('get-email', get_email),
    path('', include("eshop_account.urls")),
    path('', include("eshop_product.urls")),
    path('', include("eshop_order.urls")),
    path('', include("eshop_contact.urls")),
    path('', include("eshop_wish_list.urls")),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
