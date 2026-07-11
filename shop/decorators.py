from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def custom_login_required(view_func):
    """
    Custom login required decorator that redirects to your custom login page
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to access this page.")
            return redirect('shop:website_login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Seller required decorator

def seller_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.error(request, "Please login first.")
            return redirect("shop:website_login")

        if not hasattr(request.user, "seller"):
            messages.error(request, "You are not registered as a seller.")
            return redirect("shop:become_seller")

        if not request.user.seller.is_approved:
            messages.warning(request, "Your seller account is awaiting admin approval.")
            return redirect("shop:seller_success")

        return view_func(request, *args, **kwargs)

    return wrapper