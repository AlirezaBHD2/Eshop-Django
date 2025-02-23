from django.urls import path
from .views import ProductsList, product_detail, SearchProductsView, ProductsListByCategory , ProductsListByOrder, products_categories_partial

urlpatterns = [
    path('products', ProductsList.as_view()),
    path('products/orderby/<order>', ProductsListByOrder.as_view()),
    path('products/list/<category_name>', ProductsListByCategory.as_view()),
    path('products/<productId>/<name>', product_detail),
    path('products/search', SearchProductsView.as_view()),
    path('products_categories_partial', products_categories_partial, name='products_categories_partial')
]
