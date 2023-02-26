from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = "product"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # path("", views.FeaturedProduct.as_view(), name="featured"),
    path("search", views.ProductSearchView.as_view(), name='product_search'),
    path("product/detail/<int:pk>", views.ProductDetailView.as_view(), name='product_detail'),
    path("product", views.ProductListView.as_view(), name='product_list'),
    path("category/shop/<int:pk>", views.CategoryProductListView.as_view(), name='category_list'),
]