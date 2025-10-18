# MCart Testing Guide

## How to Test the Checkout Feature

### Prerequisites
1. Make sure you have products in the database:
   ```bash
   python manage.py create_products_from_images
   ```

2. Create a test user (or use existing):
   ```bash
   python manage.py createsuperuser
   ```

### Testing Steps

#### 1. Test Search Feature
1. Start the server: `python manage.py runserver`
2. Go to `http://127.0.0.1:8000`
3. Use the search bar in the navigation
4. Try searching for: "phone", "watch", "cooker", etc.
5. Test filters on the search results page

#### 2. Test Add to Cart
1. Browse products on the homepage or product list
2. Click "Add to Cart" on any product
3. Check that the cart counter updates in the navigation
4. Visit the cart page to see added items

#### 3. Test Checkout Process
1. **With items in cart and logged in:**
   - Go to cart page: `http://127.0.0.1:8000/cart/`
   - Click "Proceed to Checkout"
   - Fill in shipping details
   - Click "Place Order Securely"
   - Should redirect to order confirmation page

2. **Without login:**
   - Go to cart page
   - Click "Login to Checkout"
   - Login and get redirected back to checkout

3. **With empty cart:**
   - Clear cart items
   - Try to access checkout directly: `http://127.0.0.1:8000/checkout/`
   - Should redirect to cart with error message

#### 4. Test Order Management
1. After placing an order:
   - Check order confirmation page
   - Go to "My Orders" from user dropdown
   - Click on order to see details
   - Check admin panel for order management

### Test Accounts
- **Admin**: username: `admin`, password: `admin123`
- **Test User**: Create your own or use existing

### Expected Behavior

#### Search Feature ✅
- Multi-field search (name, description, category)
- Filters by category, price range
- Sorting options
- Pagination
- Grid/List view toggle

#### Checkout Process ✅
- Login required
- Form validation
- Order creation
- Email confirmation (console output)
- Order tracking
- Admin management

#### Error Handling ✅
- Empty cart protection
- Login requirement
- Form validation
- User-friendly error messages

### Troubleshooting

#### Common Issues:
1. **"Proceed to Checkout" not working**
   - Make sure user is logged in
   - Check that cart has items
   - Verify ALLOWED_HOSTS includes '127.0.0.1'

2. **Template errors**
   - Check for syntax errors in templates
   - Ensure all template filters are valid

3. **Database errors**
   - Run migrations: `python manage.py migrate`
   - Check database connection

#### Debug Commands:
```bash
# Check system
python manage.py check

# Check products
python manage.py shell -c "from shop.models import Product; print(f'Products: {Product.objects.count()}')"

# Check users
python manage.py shell -c "from django.contrib.auth.models import User; print(f'Users: {User.objects.count()}')"

# Check orders
python manage.py shell -c "from shop.models import Order; print(f'Orders: {Order.objects.count()}')"
```

### Success Criteria
- ✅ Search works with filters and sorting
- ✅ Add to cart updates cart counter
- ✅ Checkout requires login
- ✅ Order placement creates order record
- ✅ Order confirmation page displays
- ✅ Order appears in user's order history
- ✅ Admin can manage orders

## Ready for Production! 🚀

Once all tests pass, your MCart e-commerce platform is ready for deployment with full search and checkout functionality!