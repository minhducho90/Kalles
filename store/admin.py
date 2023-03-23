from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category_name']
    search_fields = ['name']

    def category_name(self, subcategory):
        return subcategory.category.name


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['subcategory']

    list_display = ['name', 'price', 'viewed_status', 'insert_date', 'subcategory_name']
    list_editable = ['price']
    list_filter = ['insert_date', 'subcategory', 'viewed']
    search_fields = ['name']
    list_per_page = 20
    ordering = ['name']

    def subcategory_name(self, product):
        return product.subcategory.name

    def viewed_status(self, product):
        if product.viewed == 0:
            return 'No'
        return 'Yes'