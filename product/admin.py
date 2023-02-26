from django.contrib import admin
from . import models

class InformationAdmin(admin.StackedInline):
    model = models.Information

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "parent")

class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 0

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", 'image',)
    list_filter = (['status'])
    search_fields = ('title',)
    inlines = (InformationAdmin, CommentInline)





admin.site.register(models.Size)
admin.site.register(models.Color)