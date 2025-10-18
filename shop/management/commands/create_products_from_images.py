import os
from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product, Category
from django.utils.text import slugify
import shutil
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create products from existing images in media/shop/images'

    def handle(self, *args, **options):
        # Define product data based on image names
        products_data = {
            'BLACK-GOLD-MENS-ACCESSORIES-G-SHOCK-WATCHES-GM110G-1A9BGLD_1.jpg': {
                'name': 'G-Shock Black Gold Watch GM110G',
                'description': 'Premium G-Shock watch with black and gold design. Durable, water-resistant, and stylish timepiece perfect for any occasion.',
                'short_description': 'Premium G-Shock watch with black and gold design',
                'price': Decimal('15999.00'),
                'discount_price': Decimal('12999.00'),
                'stock': 25,
                'category_name': 'Watches & Accessories',
                'is_featured': True,
                'rating': Decimal('4.5')
            },
            'carpet.jpg': {
                'name': 'Premium Home Carpet',
                'description': 'High-quality carpet perfect for living rooms and bedrooms. Soft texture, durable material, and elegant design.',
                'short_description': 'High-quality carpet for home decoration',
                'price': Decimal('4999.00'),
                'discount_price': Decimal('3999.00'),
                'stock': 15,
                'category_name': 'Home & Garden',
                'is_featured': False,
                'rating': Decimal('4.2')
            },
            'cooker.jpg': {
                'name': 'Electric Rice Cooker',
                'description': 'Multi-function electric rice cooker with steaming capability. Perfect for cooking rice, steaming vegetables, and more.',
                'short_description': 'Multi-function electric rice cooker',
                'price': Decimal('2999.00'),
                'discount_price': Decimal('2499.00'),
                'stock': 30,
                'category_name': 'Kitchen Appliances',
                'is_featured': True,
                'rating': Decimal('4.3')
            },
            'deo.jpg': {
                'name': 'Premium Deodorant Spray',
                'description': 'Long-lasting deodorant spray with fresh fragrance. 24-hour protection against odor and sweat.',
                'short_description': 'Long-lasting deodorant spray with fresh fragrance',
                'price': Decimal('299.00'),
                'discount_price': Decimal('249.00'),
                'stock': 100,
                'category_name': 'Personal Care',
                'is_featured': False,
                'rating': Decimal('4.0')
            },
            'hairdryer.jpg': {
                'name': 'Professional Hair Dryer',
                'description': 'Professional-grade hair dryer with multiple heat settings. Fast drying with ionic technology for smooth, shiny hair.',
                'short_description': 'Professional hair dryer with ionic technology',
                'price': Decimal('1999.00'),
                'discount_price': Decimal('1599.00'),
                'stock': 20,
                'category_name': 'Personal Care',
                'is_featured': False,
                'rating': Decimal('4.1')
            },
            'lotus.jpg': {
                'name': 'Lotus Flower Decoration',
                'description': 'Beautiful artificial lotus flower decoration. Perfect for home decor, meditation spaces, and special occasions.',
                'short_description': 'Beautiful artificial lotus flower decoration',
                'price': Decimal('599.00'),
                'discount_price': Decimal('449.00'),
                'stock': 50,
                'category_name': 'Home & Garden',
                'is_featured': False,
                'rating': Decimal('4.4')
            },
            'oneplus.png': {
                'name': 'OnePlus Smartphone',
                'description': 'Latest OnePlus smartphone with flagship features. High-performance processor, excellent camera, and fast charging.',
                'short_description': 'Latest OnePlus smartphone with flagship features',
                'price': Decimal('45999.00'),
                'discount_price': Decimal('42999.00'),
                'stock': 10,
                'category_name': 'Electronics',
                'is_featured': True,
                'rating': Decimal('4.6')
            }
        }

        # Create categories first
        categories_created = set()
        for product_data in products_data.values():
            category_name = product_data['category_name']
            if category_name not in categories_created:
                category, created = Category.objects.get_or_create(
                    name=category_name,
                    defaults={
                        'slug': slugify(category_name),
                        'description': f'{category_name} products',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'Created category: {category_name}')
                categories_created.add(category_name)

        # Create products
        source_dir = os.path.join(settings.MEDIA_ROOT, 'shop', 'images')
        dest_dir = os.path.join(settings.MEDIA_ROOT, 'products', 'main')
        
        # Create destination directory if it doesn't exist
        os.makedirs(dest_dir, exist_ok=True)

        for image_filename, product_data in products_data.items():
            source_path = os.path.join(source_dir, image_filename)
            
            if os.path.exists(source_path):
                # Check if product already exists
                if Product.objects.filter(name=product_data['name']).exists():
                    self.stdout.write(f'Product already exists: {product_data["name"]}')
                    continue

                # Copy image to products directory
                dest_filename = f"{slugify(product_data['name'])}{os.path.splitext(image_filename)[1]}"
                dest_path = os.path.join(dest_dir, dest_filename)
                shutil.copy2(source_path, dest_path)

                # Get category
                category = Category.objects.get(name=product_data['category_name'])

                # Create product
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=slugify(product_data['name']),
                    description=product_data['description'],
                    short_description=product_data['short_description'],
                    price=product_data['price'],
                    discount_price=product_data['discount_price'],
                    stock=product_data['stock'],
                    category=category,
                    main_image=f"products/main/{dest_filename}",
                    status='published',
                    is_featured=product_data['is_featured'],
                    rating=product_data['rating']
                )

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created product: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Image not found: {image_filename}')
                )

        self.stdout.write(
            self.style.SUCCESS('Product creation completed!')
        )