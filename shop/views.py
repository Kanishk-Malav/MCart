from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Wishlist, Address
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.db import OperationalError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from rest_framework import generics, permissions
from .models import Seller
from .serializers import SellerSerializer
from .forms import SellerForm, ProductForm
from .decorators import seller_required
from django.core.paginator import Paginator


def website_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)  # logs in user for Django session
            return redirect('shop:home')
        else:
            # Return the form with errors
            return render(request, 'shop/login.html', {
                'form': form,
                'error': 'Invalid username or password.'
            })
    else:
        # GET request - show empty form
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

# Logout view for website authentication
def website_logout(request):
    django_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('shop:home')


# API Views
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Authenticate and log in the user
            user = authenticate(
                username=request.data.get('username'),
                password=request.data.get('password')
            )
            if user:
                login(request, user)  # This logs in the user for Django session
                
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Accept both JSON and form POST
        username = request.data.get('username') or request.POST.get('username')
        password = request.data.get('password') or request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)  # Django session login
            refresh = RefreshToken.for_user(user)
            # If template form, redirect instead of returning JSON
            if not request.content_type == 'application/json':
                return redirect('shop:home')
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        if not request.content_type == 'application/json':
            return render(request, 'shop/login.html', {'error': 'Invalid Credentials'})
        return Response({'error': 'Invalid Credentials'}, status=401)
class LogoutView(APIView):
    def post(self, request):
        # For JWT, client just discards the token
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Regular Views
def index(request):
    try:
        categories = Category.objects.filter(is_active=True)
        featured_products = Product.objects.filter(
            status='published', 
            is_featured=True
        )[:8]
        context = {
            'categories': categories,
            'featured_products': featured_products
        }
    except OperationalError:
        context = {
            'categories': [],
            'featured_products': []
        }
    return render(request, 'shop/index.html', context)

def product_list(request, category_slug=None):
    try:
        category = None
        categories = Category.objects.filter(is_active=True)
        products = Product.objects.filter(status='published')
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        
        context = {
            'category': category,
            'categories': categories,
            'products': products
        }
    except OperationalError:
        context = {
            'category': None,
            'categories': [],
            'products': []
        }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, 
        id=id, 
        slug=slug, 
        status='published'
    )
    related_products = Product.objects.filter(
        category=product.category, 
        status='published'
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/product_detail.html', context)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

def tracker(request):
    return render(request, 'shop/tracker.html')

def search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'relevance')
    
    products = Product.objects.filter(status='published')
    
    if query:
        # Enhanced search with multiple fields
        products = products.filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query) |
            models.Q(short_description__icontains=query) |
            models.Q(category__name__icontains=query)
        ).distinct()
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if min_price:
        try:
            min_price_val = float(min_price)
            products = products.filter(price__gte=min_price_val)
        except ValueError:
            pass
    
    if max_price:
        try:
            max_price_val = float(max_price)
            products = products.filter(price__lte=max_price_val)
        except ValueError:
            pass
    
    # Sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # relevance
        if query:
            # Simple relevance scoring - products with query in name get priority
            products = products.extra(
                select={
                    'relevance': "CASE WHEN shop_product.name ILIKE %s THEN 1 ELSE 0 END"
                },
                select_params=[f'%{query}%']
            ).order_by('-relevance', 'name')
        else:
            products = products.order_by('-created_at')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'total_results': products.count(),
    }
    return render(request, 'shop/search.html', context)

# Cart Views
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, status='published')
    
    # Check if product is in stock
    if product.stock <= 0:
        messages.error(request, f"{product.name} is out of stock")
        return redirect('shop:product_detail', id=product.id, slug=product.slug)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get quantity from POST data (from product detail form) or default to 1
    quantity = int(request.POST.get('quantity', 1))
    
    # Ensure quantity doesn't exceed stock
    if quantity > product.stock:
        quantity = product.stock
        messages.warning(request, f"Only {product.stock} items available. Added {quantity} to cart.")
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Check if adding more would exceed stock
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            cart_item.quantity = product.stock
            messages.warning(request, f"Cart updated to maximum available quantity: {product.stock}")
        else:
            cart_item.quantity = new_quantity
            messages.success(request, f"Added {quantity} more {product.name} to cart")
        cart_item.save()
    else:
        messages.success(request, f"Added {quantity} {product.name} to cart")
    
    # Redirect back to the referring page or cart
    next_url = request.POST.get('next', request.GET.get('next', 'shop:view_cart'))
    return redirect(next_url)

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated")
    else:
        cart_item.delete()
        messages.success(request, "Item removed")
    
    return redirect('shop:view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart")
    return redirect('shop:view_cart')

# Seller Views
# In views.py - REPLACE the duplicate become_seller functions with this single version:
@login_required
def become_seller(request):
    # Check if user is already a seller
    if hasattr(request.user, 'seller'):
        messages.info(request, "You are already a seller!")
        return redirect('shop:home')
    
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()
            messages.success(request, "Seller application submitted successfully!")
            return redirect('shop:seller_success')
    else:
        form = SellerForm()
    
    return render(request, 'shop/seller/become_seller.html', {'form': form})

@login_required
def seller_success(request):
    return render(request, 'shop/seller/seller_success.html')


# Seller Display Views
def seller_list(request):
    """Display all approved sellers"""
    sellers = Seller.objects.filter(is_approved=True).select_related('user')
    context = {
        'sellers': sellers
    }
    return render(request, 'shop/seller/seller_list.html', context)

def seller_detail(request, seller_id):
    """Display individual seller details"""
    seller = get_object_or_404(Seller, id=seller_id, is_approved=True)
    context = {
        'seller': seller
    }
    return render(request, 'shop/seller/seller_detail.html', context)

@login_required
@seller_required
def seller_dashboard(request):
    """Dashboard for sellers to manage their profile"""
    seller = request.user.seller 
    context = {
        'seller': seller
    }
    return render(request, 'shop/seller/seller_dashboard.html', context)

@login_required
@seller_required
def seller_add_product(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            product = form.save(commit=False)

            # Very Important
            product.seller = request.user.seller
            product.save()
            form.save_m2m()

            messages.success(
                request,
                "Product added successfully."
            )
            return redirect("shop:seller_products")
        
    else:
        form = ProductForm()
    return render(
        request,
        "shop/seller/add_product.html",
        {
            "form": form
        }
    )

@login_required
@seller_required
def seller_products(request):

    search = request.GET.get("search", "")

    products = Product.objects.filter(
        seller=request.user.seller
    ).select_related(
        "category"
    ).prefetch_related(
        "images"
    )

    if search:
        products = products.filter(
            models.Q(name__icontains=search) |
            models.Q(sku__icontains=search)
        )

    paginator = Paginator(
        products.order_by("-created_at"),
        10
    )

    page = request.GET.get("page")

    products = paginator.get_page(page)

    context = {
        "products": products,
        "search": search,
    }

    return render(
        request,
        "shop/seller/product_list.html",
        context
    )

@login_required
@seller_required
def seller_edit_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        seller=request.user.seller
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect("shop:seller_products")

    else:

        form = ProductForm(instance=product)

    return render(
        request,
        "shop/seller/edit_product.html",
        {
            "form": form,
            "product": product
        }
    )

@login_required
@seller_required
def seller_delete_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        seller=request.user.seller
    )

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

        return redirect("shop:seller_products")

    return redirect("shop:seller_products")

# Checkout and Order Views
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if not cart.items.exists():
        messages.error(request, "Your cart is empty")
        return redirect('shop:view_cart')
    
    # Get user's addresses
    addresses = request.user.addresses.all()
    
    if request.method == 'POST':
        # Process checkout
        shipping_name = request.POST.get('shipping_name')
        shipping_email = request.POST.get('shipping_email')
        shipping_phone = request.POST.get('shipping_phone')
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_state = request.POST.get('shipping_state')
        shipping_postal_code = request.POST.get('shipping_postal_code')
        
        # Calculate totals
        subtotal = cart.total_price
        shipping_cost = Decimal('50.00') if subtotal < 500 else Decimal('0.00')  # Free shipping over ₹500
        tax_amount = subtotal * Decimal('0.18')  # 18% GST
        total_amount = subtotal + shipping_cost + tax_amount
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_name=shipping_name,
            shipping_email=shipping_email,
            shipping_phone=shipping_phone,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_postal_code=shipping_postal_code,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status='confirmed',
            payment_status='completed'  # Assuming COD for now
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.current_price
            )
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        # Send order confirmation email (optional)
        try:
            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            
            subject = f'Order Confirmation - #{order.order_number}'
            message = render_to_string('shop/emails/order_confirmation.txt', {
                'order': order,
                'user': request.user
            })
            send_mail(
                subject,
                message,
                'noreply@mcart.com',
                [order.shipping_email],
                fail_silently=True
            )
        except Exception as e:
            # Log error but don't fail the order
            print(f"Failed to send order confirmation email: {e}")
        
        messages.success(request, f"🎉 Order #{order.order_number} placed successfully! You will receive a confirmation email shortly.")
        return redirect('shop:order_confirmation', order_number=order.order_number)
    
    subtotal = cart.total_price
    shipping_cost = Decimal('50.00') if subtotal < 500 else Decimal('0.00')
    tax_amount = subtotal * Decimal('0.18')
    free_shipping_remaining = max(0, 500 - float(subtotal)) if subtotal < 500 else 0
    
    context = {
        'cart': cart,
        'addresses': addresses,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'tax_amount': tax_amount,
        'free_shipping_remaining': free_shipping_remaining,
    }
    return render(request, 'shop/checkout.html', context)

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_list.html', {'orders': orders})

# Wishlist Views
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'shop/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f"Added {product.name} to wishlist")
    else:
        messages.info(request, f"{product.name} is already in your wishlist")
    
    return redirect('shop:product_detail', id=product.id, slug=product.slug)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"Removed {product.name} from wishlist")
    return redirect('shop:wishlist')

# User Profile Views
@login_required
def user_profile(request):
    addresses = request.user.addresses.all()
    recent_orders = Order.objects.filter(user=request.user)[:5]
    
    context = {
        'addresses': addresses,
        'recent_orders': recent_orders,
    }
    return render(request, 'shop/user_profile.html', context)

@login_required
def add_address(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            type=request.POST.get('type', 'home'),
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address_line_1=request.POST.get('address_line_1'),
            address_line_2=request.POST.get('address_line_2', ''),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            is_default=request.POST.get('is_default') == 'on'
        )
        messages.success(request, "Address added successfully!")
        return redirect('shop:user_profile')
    
    return render(request, 'shop/add_address.html')

# Search and Filter Views
def advanced_search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.filter(status='published')
    
    if query:
        products = products.filter(
            models.Q(name__icontains=query) | 
            models.Q(description__icontains=query) |
            models.Q(short_description__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'shop/advanced_search.html', context)

@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    # Mark as recently placed (for special styling)
    recently_placed = True
    
    context = {
        'order': order,
        'recently_placed': recently_placed,
    }
    return render(request, 'shop/order_confirmation.html', context)