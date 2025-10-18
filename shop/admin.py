from django.contrib import admin
from .models import (Category, Product, ProductImage, 
                    ProductTag, ProductReview, Cart, CartItem, Seller,
                    Order, OrderItem, Wishlist, Address)
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

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'user', 'phone', 'is_approved', 'user__date_joined']
    list_filter = ['is_approved', 'user__date_joined']
    search_fields = ['store_name', 'user__username', 'user__email', 'phone']
    list_editable = ['is_approved']
    readonly_fields = ['user']
    
    fieldsets = (
        ('Store Information', {
            'fields': ('user', 'store_name', 'store_description')
        }),
        ('Contact Details', {
            'fields': ('address', 'phone')
        }),
        ('Status', {
            'fields': ('is_approved',)
        }),
    )
    
    def user__date_joined(self, obj):
        return obj.user.date_joined.strftime('%Y-%m-%d')
    user__date_joined.short_description = 'Applied Date'
    user__date_joined.admin_order_field = 'user__date_joined'

# Order Management
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'total_price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email', 'shipping_name']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_editable = ['status', 'payment_status']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Shipping Details', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 
                      'shipping_address', 'shipping_city', 'shipping_state', 
                      'shipping_postal_code', 'shipping_country')
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'total_amount')
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'estimated_delivery')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['order__order_number', 'product__name']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'type', 'city', 'state', 'is_default']
    list_filter = ['type', 'is_default', 'state']
    search_fields = ['user__username', 'name', 'city']