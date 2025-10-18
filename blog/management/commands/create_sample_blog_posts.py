from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create sample blog posts and categories'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {
                'name': 'Shopping Tips',
                'description': 'Tips and tricks for smart shopping'
            },
            {
                'name': 'Product Reviews',
                'description': 'Detailed reviews of our products'
            },
            {
                'name': 'Technology',
                'description': 'Latest tech trends and gadgets'
            },
            {
                'name': 'Lifestyle',
                'description': 'Lifestyle and home improvement tips'
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Get or create admin user for blog posts
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@mcart.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Created admin user')

        # Sample blog posts
        posts_data = [
            {
                'title': '10 Smart Shopping Tips to Save Money',
                'content': '''Shopping smart doesn't just mean finding the lowest prices. It's about getting the best value for your money while ensuring you're buying quality products that meet your needs.

Here are our top 10 tips for smart shopping:

1. **Make a List and Stick to It**: Before you start shopping, make a list of what you actually need. This helps prevent impulse purchases.

2. **Compare Prices**: Don't settle for the first price you see. Use price comparison tools and check multiple retailers.

3. **Look for Sales and Discounts**: Sign up for newsletters and follow your favorite stores on social media to stay informed about sales.

4. **Read Reviews**: Before making a purchase, especially for expensive items, read customer reviews to understand the product's quality and performance.

5. **Consider the Total Cost**: Factor in shipping, taxes, and any additional fees when comparing prices.

6. **Buy in Season**: Purchase seasonal items when they're in season for better prices and selection.

7. **Use Cashback and Reward Programs**: Take advantage of cashback credit cards and store loyalty programs.

8. **Check Return Policies**: Make sure you understand the return policy before making a purchase.

9. **Buy Quality Over Quantity**: Sometimes it's better to spend more on a quality item that will last longer.

10. **Set a Budget**: Determine how much you can afford to spend and stick to it.

Remember, the goal is to make informed decisions that provide the best value for your money!''',
                'excerpt': 'Learn how to shop smarter and save money with these 10 essential tips that every savvy shopper should know.',
                'category': 'Shopping Tips',
                'is_featured': True
            },
            {
                'title': 'G-Shock GM110G Review: The Perfect Blend of Style and Durability',
                'content': '''The G-Shock GM110G Black Gold Watch represents the perfect marriage of rugged functionality and sophisticated style. After testing this timepiece for several weeks, here's our comprehensive review.

**Design and Build Quality**
The GM110G features a striking black and gold color scheme that immediately catches the eye. The case is constructed from G-Shock's signature resin material, providing excellent shock resistance while maintaining a comfortable weight on the wrist.

**Features**
- Water resistance up to 200 meters
- World time with 31 time zones
- Stopwatch function
- Countdown timer
- 5 daily alarms
- Auto LED backlight

**Performance**
In our testing, the watch performed flawlessly. The timekeeping is accurate, and all functions work as expected. The LED backlight is particularly useful in low-light conditions.

**Pros:**
- Excellent build quality
- Stylish design
- Comprehensive feature set
- Great value for money

**Cons:**
- Can be bulky for smaller wrists
- Digital display might not appeal to everyone

**Verdict**
The G-Shock GM110G is an excellent choice for anyone looking for a durable, feature-rich watch that doesn't compromise on style. At its current price point, it offers exceptional value.

Rating: 4.5/5 stars''',
                'excerpt': 'Our detailed review of the G-Shock GM110G Black Gold Watch - a perfect blend of durability and style.',
                'category': 'Product Reviews',
                'is_featured': True
            },
            {
                'title': 'The Rise of Smart Home Appliances in 2024',
                'content': '''Smart home technology has evolved dramatically in recent years, and 2024 is shaping up to be a pivotal year for smart appliances. From intelligent rice cookers to AI-powered hair dryers, the integration of technology into everyday appliances is transforming how we interact with our homes.

**What Makes an Appliance "Smart"?**
Smart appliances are connected devices that can be controlled remotely, learn from user behavior, and integrate with other smart home systems. They typically feature:
- Wi-Fi connectivity
- Mobile app control
- Voice assistant integration
- Automated scheduling
- Energy monitoring

**Popular Smart Appliances in 2024**
1. **Smart Rice Cookers**: These can be programmed remotely and adjust cooking times based on rice type and quantity.
2. **Intelligent Hair Dryers**: Feature heat sensors and automatic shut-off for hair protection.
3. **Connected Kitchen Scales**: Sync with recipe apps for precise measurements.

**Benefits of Smart Appliances**
- Convenience and remote control
- Energy efficiency
- Improved safety features
- Better performance through AI learning

**The Future**
As IoT technology continues to advance, we can expect even more sophisticated smart appliances that seamlessly integrate into our daily routines.''',
                'excerpt': 'Explore how smart home appliances are revolutionizing our daily lives in 2024.',
                'category': 'Technology',
                'is_featured': False
            },
            {
                'title': 'Creating a Cozy Home Environment with the Right Decor',
                'content': '''Your home should be your sanctuary - a place where you can relax, recharge, and feel completely comfortable. Creating a cozy atmosphere doesn't require a complete renovation or a huge budget. Sometimes, small changes can make a big difference.

**Essential Elements for a Cozy Home**

**1. Soft Textures**
Incorporate soft textures through carpets, throw pillows, and blankets. A premium carpet can instantly warm up a room and provide comfort underfoot.

**2. Warm Lighting**
Replace harsh overhead lighting with warm, ambient lighting. Table lamps, floor lamps, and candles can create a welcoming atmosphere.

**3. Natural Elements**
Bring nature indoors with plants, flowers, or natural decorative elements like lotus flowers. These add life and freshness to any space.

**4. Personal Touches**
Display items that have personal meaning - family photos, artwork, or collections that reflect your personality.

**5. Comfortable Seating**
Invest in comfortable furniture where you can truly relax. This might be a cozy armchair or a plush sofa.

**Budget-Friendly Tips**
- Rearrange existing furniture for better flow
- Add plants for natural beauty
- Use warm-colored light bulbs
- Incorporate soft textiles
- Declutter for a cleaner, more peaceful environment

Remember, the goal is to create a space that feels uniquely yours and promotes relaxation and happiness.''',
                'excerpt': 'Transform your living space into a cozy sanctuary with these simple yet effective decorating tips.',
                'category': 'Lifestyle',
                'is_featured': False
            }
        ]

        for post_data in posts_data:
            category = Category.objects.get(name=post_data['category'])
            
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'slug': slugify(post_data['title']),
                    'author': admin_user,
                    'category': category,
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'status': 'published',
                    'is_featured': post_data['is_featured']
                }
            )
            if created:
                self.stdout.write(f'Created post: {post.title}')

        self.stdout.write(
            self.style.SUCCESS('Sample blog content created successfully!')
        )