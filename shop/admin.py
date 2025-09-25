from django.contrib import admin
from .models import (Category, Product, ProductImage, 
                    ProductTag, ProductReview, Cart, CartItem)
from django.utils.html import format_html

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['thumbnail']
    
    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
        return ''
    
    class Media:
        css = {
            'all': ['shop/css/admin-thumbnails.css']
        }

class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ['user', 'product', 'rating', 'title', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'current_price', 'stock', 
                   'status', 'is_featured', 'rating', 'created_at')
    list_filter = ('status', 'category', 'is_featured', 'created_at')
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'rating')
    inlines = [ProductImageInline, ProductReviewInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'description', 
                      'short_description', 'tags')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price', 'cost_price')
        }),
        ('Inventory', {
            'fields': ('stock', 'weight')
        }),
        ('Status & Visibility', {
            'fields': ('status', 'is_featured', 'is_bestseller')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'thumbnail', 'is_default', 'order')
    list_editable = ('is_default', 'order')
    list_filter = ('product', 'is_default')
    
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')
    thumbnail.short_description = 'Image'

@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 
                   'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('product__name', 'user__username', 'title')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_approved',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'total_price']
    list_filter = ['created_at', 'updated_at']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']
    list_filter = ['cart__user']