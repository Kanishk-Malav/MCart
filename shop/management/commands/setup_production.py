from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product
from blog.models import Category as BlogCategory, Post
from django.utils.text import slugify
import os

class Command(BaseCommand):
    help = 'Setup production data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up production environment...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@mcart.com',
                password=os.environ.get('ADMIN_PASSWORD', 'admin123')
            )
            self.stdout.write('Created superuser')
        
        # Create sample categories if none exist
        if not Category.objects.exists():
            categories = [
                'Electronics', 'Fashion', 'Home & Garden', 
                'Sports', 'Books', 'Health & Beauty'
            ]
            for cat_name in categories:
                Category.objects.create(
                    name=cat_name,
                    slug=slugify(cat_name),
                    description=f'{cat_name} products',
                    is_active=True
                )
            self.stdout.write('Created sample categories')
        
        # Create blog categories if none exist
        if not BlogCategory.objects.exists():
            blog_categories = [
                'Shopping Tips', 'Product Reviews', 'Technology', 'Lifestyle'
            ]
            for cat_name in blog_categories:
                BlogCategory.objects.create(
                    name=cat_name,
                    slug=slugify(cat_name),
                    description=f'{cat_name} blog posts'
                )
            self.stdout.write('Created blog categories')
        
        # Create logs directory
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        self.stdout.write('Created logs directory')
        
        self.stdout.write(
            self.style.SUCCESS('Production setup completed successfully!')
        )