from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Initialize shop data'

    def handle(self, *args, **options):
        # Create sample categories
        electronics = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Electronic gadgets'
        )
        
        # Create sample products
        Product.objects.create(
            name='Smartphone',
            slug='smartphone',
            category=electronics,
            description='Latest smartphone',
            price=599.99,
            discount_price=549.99,
            is_featured=True,
            status='published',
            main_image='products/main/smartphone.jpg'
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized shop data'))