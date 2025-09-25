from django.core.management.base import BaseCommand
from shop.models import Category, Product, ProductTag
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates the database with sample products and categories'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            'Electronics', 'Clothing', 'Home & Kitchen', 
            'Books', 'Sports', 'Beauty'
        ]
        
        for cat_name in categories:
            Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'description': f"All {cat_name} products",
                    'is_active': True
                }
            )
        
        # Create tags
        tags = [
            'Featured', 'New Arrival', 'Best Seller', 
            'On Sale', 'Eco Friendly', 'Limited Edition'
        ]
        
        for tag_name in tags:
            ProductTag.objects.get_or_create(name=tag_name)
        
        # Create sample products
        products_data = [
            {'name': 'Wireless Headphones', 'category': 'Electronics', 'price': 99.99},
            {'name': 'Smart Watch', 'category': 'Electronics', 'price': 199.99, 'discount_price': 149.99},
            {'name': 'Cotton T-Shirt', 'category': 'Clothing', 'price': 19.99},
            {'name': 'Non-Stick Pan', 'category': 'Home & Kitchen', 'price': 29.99},
            {'name': 'Python Programming Book', 'category': 'Books', 'price': 39.99},
            {'name': 'Yoga Mat', 'category': 'Sports', 'price': 24.99, 'discount_price': 19.99},
            {'name': 'Face Cream', 'category': 'Beauty', 'price': 14.99},
        ]
        
        for product_data in products_data:
            category = Category.objects.get(name=product_data['category'])
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'category': category,
                    'description': f"High quality {product_data['name']}",
                    'short_description': f"Best {product_data['name']} in the market",
                    'price': product_data['price'],
                    'discount_price': product_data.get('discount_price'),
                    'stock': random.randint(10, 100),
                    'status': 'published',
                    'is_featured': random.choice([True, False]),
                }
            )
            
            # Add random tags
            all_tags = list(ProductTag.objects.all())
            tags_to_add = random.sample(all_tags, min(3, len(all_tags)))
            product.tags.set(tags_to_add)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated sample data'))