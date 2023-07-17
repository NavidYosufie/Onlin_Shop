from django.urls import path
from . import views
# from django.views.decorators.cache import cache_page

app_name = "product"

urlpatterns = [
    path("",(views.HomeView.as_view()), name="home"),
    path("navbar",(views.NavbarPartialView.as_view()), name="navbar"),
    # path("", views.FeaturedProduct.as_view(), name="featured"),
    path("search", views.ProductSearchView.as_view(), name='product_search'),
    path("product/detail/<int:pk>", views.ProductDetailCommentView.as_view(), name='product_detail'),
    path("product", views.ProductListView.as_view(), name='product_list'),
    path("category/shop/<slug:slug>", views.Category_Ditael.as_view(), name='category_list')
]