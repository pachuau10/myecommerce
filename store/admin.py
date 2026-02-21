from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Review, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_featured', 'is_new']
    list_filter = ['category', 'is_featured', 'is_new']
    list_editable = ['price', 'stock', 'is_featured', 'is_new']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    inlines = [OrderItemInline]


admin.site.register(Review)
admin.site.register(Wishlist)
