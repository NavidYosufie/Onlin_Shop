from django.db.models import Count

from cart.models import Order, OrderItem
from product.models import Category, Product


# def cateqouries(request):
#     category = Category.objects.filter(parent=None)
#     return {"cateqouries": category}

def number_product_user(request):
    order = OrderItem.objects.all()
    return {'number_product': order}

def featured_category(request):
    category = Category.objects.filter(featured=True).order_by('-created_at')[:3]
    return {"fc": category}

def featured_product_list(request):
    featured = Product.objects.filter(featured=True)
    return {"fp": featured}

def recent_product(request):
    recent_product_list = Product.objects.filter(status=True).order_by('-created_at')[:15]
    return {"rp": recent_product_list}

def featured_product(request):
    featured = Product.objects.filter(featured=True).order_by('-created_at')
    return {"fp_s": featured}