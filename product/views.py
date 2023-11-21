from django.views.generic import TemplateView, ListView
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Comment
from django.core.paginator import Paginator
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
    paginate_by = 6
    model = Product
    template_name = 'product/products_list.html'

    def get_context_data(self, **kwargs):
        request = self.request
        search = request.GET.get('q')
        product = Product.objects.filter(title__iexact=search)
        context = super(ProductSearchView, self).get_context_data()
        paginator = Paginator(product, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['object_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'product/products_list.html'
    paginate_by = 6

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

        paginator = Paginator(queryset, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = super(ProductListView, self).get_context_data()
        context['object_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        return context


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
