from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, FormView
from django.views.generic.detail import DetailView, SingleObjectMixin
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
        query = self.request.GET.get("q")
        object_list = Product.objects.filter(title__icontains=query)
        print(object_list)
        return object_list


class ProductListView(ListView):
    model = Product
    template_name = 'product/shop.html'
    context_object_name = 'product'


class ProductDetailView(View):

    def get(self, request, pk):
        global product
        product = get_object_or_404(Product, id=pk)
        comment = Comment.objects.filter(active=True)
        form = CommentForm
        context = {
            'product': product,
            'comment': comment,
            'form': form
        }
        return render(request, 'product/product_detail.html', context)

    def post(self, request, *args, **kwargs):
        comment = CommentForm(data=request.POST)
        user = request.user
        if comment.is_valid():
            cd = comment.cleaned_data
            Comment.objects.create(product=product, user=user, text=cd['text'])
            return redirect('/')




class CategoryProductListView(ListView):
    model = Product
    template_name = 'product/shop.html'
    paginate_by = 2
    context_object_name = 'product'
