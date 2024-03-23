from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import Product, Category, Order, Comment, Customer


class InventoryFilter(admin.SimpleListFilter):
    LESS_THAN_3 = '<3'
    BETWEEN_THAN_3_AND_10 = '3<=10'
    MORE_THAN_10 = '>10'
    title = 'Critical Inventory Status'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin) :
        return [
            (InventoryFilter.LESS_THAN_3, 'High'),
            (InventoryFilter.BETWEEN_THAN_3_AND_10, 'Medium'),
            (InventoryFilter.MORE_THAN_10, 'OK'),
        ]
        
    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(inventory__lt=3)
        if self.value() == InventoryFilter.BETWEEN_THAN_3_AND_10:
            return queryset.filter(inventory__range=(3, 10))
        if self.value() == InventoryFilter.MORE_THAN_10:
            return queryset.filter(inventory__gt=10)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','inventory', 'unit_price','product_category','product_comment', 'is_low']
    list_per_page = 30
    list_editable = ['unit_price']
    list_select_related = ['category']
    list_filter = ['datetime_created', InventoryFilter]
    
    def get_queryset(self, request):
        return super() \
                .get_queryset(request) \
                .prefetch_related('comments') \
                .annotate(comment_count= Count('comments'))
    
    def is_low(self, product: Product):
        if product.inventory <10:
            return 'Low'
        if product.inventory >50:
            return 'High'
        return 'Medium'
    
    @admin.display(ordering='category__title')
    def product_category(self, product:Product):
        return product.category.title
    
    @admin.display(ordering='comment_count', description='# comments')
    def product_comment(self, product:Product):
        return product.comment_count

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer', 'status','num_of_items', 'datetime_created']
    list_per_page = 30
    list_editable = ['status']
    ordering = ['-datetime_created']
    
    def get_queryset(self, request):
        return super() \
                    .get_queryset(request) \
                    .prefetch_related('items') \
                    .annotate(
                        items_count =  Count('items')
                    )
    
    @admin.display(ordering='items_count', description='# items')
    def num_of_items(self, order:Order):
        return order.items_count
        

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','product', 'status', 'datetime_created']
    list_per_page = 30
    list_editable = ['status']
    list_display_links = ['id', 'product']
    ordering = ['-datetime_created']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'phone_number']
    list_per_page = 30
    ordering = ['first_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    

admin.site.register(Category)