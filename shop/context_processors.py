from .models import Seller, Cart

def seller_context(request):
    """Add seller information to template context"""
    context = {
        'is_seller': False,
        'seller_profile': None,
        'cart_items_count': 0
    }
    
    if request.user.is_authenticated:
        # Seller context
        try:
            seller = request.user.seller
            context['is_seller'] = True
            context['seller_profile'] = seller
        except Seller.DoesNotExist:
            pass
        
        # Cart context
        try:
            cart = Cart.objects.get(user=request.user)
            context['cart_items_count'] = cart.total_items
        except Cart.DoesNotExist:
            pass
    
    return context