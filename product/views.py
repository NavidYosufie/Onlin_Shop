from django.views.generic import TemplateView, ListView
from django.shortcuts import render, get_object_or_404, redirect

from account.models import User
from cart.cart_module import Cart
from .models import Product, Category, Comment
from django.core.paginator import Paginator
from django.urls import reverse
from .forms import CommentForm
from django.views import View


class HomeView(ListView):
    model = Product
    template_name = "product/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()[:12]
        return context


class ProductSearchView(ListView):
    model = Product
    template_name = 'product/products_list.html'
    context_object_name = 'product'

    def get_queryset(self):  # new
        queryset = self.request.GET.get("q")
        object_list = Product.objects.filter(title__icontains=queryset)
        return object_list


class ProductListView(ListView):
    template_name = 'product/products_list.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        request = self.request
        colors = request.GET.getlist('color')
        sizes = request.GET.getlist('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        queryset = Product.objects.all()
        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()

        if sizes:
            queryset = queryset.filter(size__title__in=sizes).distinct()

        if min_price and max_price:
            queryset = queryset.filter(price__lte=max_price, price__gte=min_price)

        context = super(ProductListView, self).get_context_data()
        context['object_list'] = queryset
        return context

    # def get(self, request):
    #     page_number = request.GET.get('page')
    #     queryset = Product.objects.filter(status=True)
    #     pagination = Paginator(queryset, 6)
    #     object_list = pagination.get_page(page_number)
    #     return render(request, 'product/products_list.html', {'object_list': object_list})


class ProductDetailCommentView(View):

    def get(self, request, pk):
        global product
        product = get_object_or_404(Product, id=pk)
        comment = Comment.objects.filter(active=True)
        form = CommentForm
        global context
        context = {
            'product': product,
            'comment': comment,
            'form': form
        }
        return render(request, 'product/product_detail.html', context)

    def post(self, request, *args, **kwargs):
        comment = CommentForm(data=request.POST)
        user = request.user
        print(comment['text'])
        if comment.is_valid():
            cd = comment.cleaned_data
            Comment.objects.create(product=product, user=user, text=cd['text'])
        return render(request, 'product/product_detail.html', context)


class CategoryDetailView(View):
    def get(self, request, slug):
        page_number = request.GET.get("page")
        category = get_object_or_404(Category, slug=slug)
        product = category.product_set.all()
        paginator = Paginator(product, 6)
        object_list = paginator.get_page(page_number)
        return render(request, "product/products_list.html", {"object_list": object_list})


class NavbarPartialView(TemplateView, View):
    template_name = 'includes/navbar.html'

    def get_context_data(self, **kwargs):
        context = super(NavbarPartialView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context
