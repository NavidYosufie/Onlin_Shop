from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, FormView
from django.views.generic.detail import DetailView, SingleObjectMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category, Comment
from .forms import CommentForm


class HomeView(ListView):
    model = Product
    template_name = "product/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()[:12]
        return context


class ProductSearchView(ListView):
    model = Product
    template_name = 'product/shop.html'
    context_object_name = 'product'

    def get_queryset(self):  # new
        queryset = self.request.GET.get("q")
        object_list = Product.objects.filter(title__icontains=queryset)
        return object_list


class ProductListView(ListView):
    model = Product
    template_name = 'product/shop.html'
    context_object_name = 'product'
    paginate_by = 9


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


class Category_Ditael(View):
    def get(self, request, slug):
        page_number = request.GET.get("page")
        category = get_object_or_404(Category, slug=slug)
        product = category.product_set.all()
        paginator = Paginator(product, 2)
        object_list = paginator.get_page(page_number)
        return render(request, "product/shop.html", {"product": object_list})


class NavbarPartialView(TemplateView):
    template_name = 'includes/navbar.html'

    def get_context_data(self, **kwargs):
        context = super(NavbarPartialView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context
