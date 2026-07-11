from django.urls import path
from . import views
from .views import (
    RegisterView, 
    LoginView, 
    UserProfileView,
    product_list,
    product_detail,
)

app_name = 'shop'

urlpatterns = [
    # Main pages
    path('', views.index, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Other pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('tracker/', views.tracker, name='tracker'),
    path('search/', views.search, name='search'),

    # API Endpoints
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', LoginView.as_view(), name='auth_login'),
    path('api/auth/profile/', UserProfileView.as_view(), name='auth_profile'),

    # Website Authentication
    path('login/', views.website_login, name='website_login'),
    path('logout/', views.website_logout, name='website_logout'),

    # Checkout and Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('order/<str:order_number>/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_list, name='order_list'),
    
    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # User Profile
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/add-address/', views.add_address, name='add_address'),
    
    # Advanced Search
    path('search/advanced/', views.advanced_search, name='advanced_search'),
    
    # Seller
    path('become-seller/', views.become_seller, name='become_seller'),
    path('seller-success/', views.seller_success, name='seller_success'),
    path('sellers/', views.seller_list, name='seller_list'),
    path('seller/<int:seller_id>/', views.seller_detail, name='seller_detail'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path("seller/products/add/", views.seller_add_product, name="seller_add_product"),
    path("seller/products/", views.seller_products, name="seller_products"),
    path("seller/products/<int:pk>/edit/", views.seller_edit_product, name="seller_edit_product"),
    path("seller/products/<int:pk>/delete/", views.seller_delete_product, name="seller_delete_product"),
]
