from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from account.models import User


class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subs')
    title = models.CharField(max_length=100, null=True, blank=True)
    featured_title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    featured = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("product:category_list", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['parent__id']



class Product(models.Model):
    featured = models.BooleanField(default=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    discount = models.SmallIntegerField(null=True, blank=True)
    image = models.ImageField(null=True)
    size = models.ManyToManyField(Size, related_name="products", null=True, blank=True)
    color = models.ManyToManyField(Color, related_name="color", blank=True, null=True)
    status = models.BooleanField(null=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # slug = models.SlugField(null=True, blank=True)

    def get_absolut_url(self):
        return reverse('product:product_detail', kwargs={"pk": self.id})

    # def save(self):
    #     self.slug = slugify(self.title)
    #     super(Product, self).save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='comment_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user', null=True)
    text = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=False, null=True)


class Information(models.Model):
    product = models.ForeignKey(Product, related_name="information", on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.text[:30]



