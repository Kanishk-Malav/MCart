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