from django.core.management.base import BaseCommand
from shop.models import Category, Product, ProductTag

class Command(BaseCommand):
    help = 'Seeds the database with sample products and categories'
    
    def handle(self, *args, **kwargs):
        # Create categories
        electronics = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Latest electronic gadgets'
        )
        
        clothing = Category.objects.create(
            name='Clothing',
            slug='clothing',
            description='Fashionable clothing items'
        )
        
        # Create tags
        popular_tag = ProductTag.objects.create(name='Popular', slug='popular')
        new_tag = ProductTag.objects.create(name='New Arrival', slug='new-arrival')
        
        # Create sample products
        Product.objects.create(
            name='Wireless Headphones',
            slug='wireless-headphones',
            category=electronics,
            description='High-quality wireless headphones with noise cancellation',
            price=199.99,
            discount_price=179.99,
            stock=50,
            status='published',
            is_featured=True,
            tags=[popular_tag, new_tag]
        )
        
        Product.objects.create(
            name='Smart Watch',
            slug='smart-watch',
            category=electronics,
            description='Feature-packed smartwatch with health monitoring',
            price=299.99,
            stock=30,
            status='published',
            is_bestseller=True
        )
        
        Product.objects.create(
            name='Cotton T-Shirt',
            slug='cotton-tshirt',
            category=clothing,
            description='Comfortable 100% cotton t-shirt',
            price=24.99,
            discount_price=19.99,
            stock=100,
            status='published'
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))