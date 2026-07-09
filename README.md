# 🛒 MCart - Full-Featured E-commerce Platform

[![Django](https://img.shields.io/badge/Django-5.1.3-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

MCart is a complete e-commerce solution built with Django, featuring everything you need to run an online marketplace like Amazon or Flipkart. Built with modern web technologies and production-ready features.

## 🚀 Features

### Core E-commerce Features
- **Product Management**: Categories, products, variants, inventory tracking
- **Shopping Cart**: Add to cart, quantity management, persistent cart
- **Checkout Process**: Multi-step checkout with address management
- **Order Management**: Order tracking, status updates, order history
- **User Accounts**: Registration, login, profile management, address book
- **Wishlist**: Save products for later
- **Search & Filters**: Advanced product search and filtering
- **Reviews & Ratings**: Product reviews and rating system

### Seller Features
- **Seller Registration**: Become a seller application process
- **Seller Dashboard**: Manage products and orders
- **Multi-vendor Support**: Multiple sellers can list products

### Content Management
- **Blog System**: Full-featured blog with categories and comments
- **CMS Pages**: About, Contact, Terms, Privacy pages

### Admin Features
- **Comprehensive Admin Panel**: Manage all aspects of the platform
- **Order Management**: Process orders, update status, track shipments
- **User Management**: Manage customers and sellers
- **Analytics Dashboard**: Sales reports and analytics

### Technical Features
- **REST API**: Complete API for mobile apps and integrations
- **JWT Authentication**: Secure token-based authentication
- **Responsive Design**: Mobile-first responsive design
- **SEO Optimized**: SEO-friendly URLs and meta tags
- **Security**: CSRF protection, XSS protection, secure headers

## 🛠️ Technology Stack

- **Backend**: Django 5.1.3, Django REST Framework
- **Database**: PostgreSQL (production), SQLite (development)
- **Frontend**: Bootstrap 5, JavaScript
- **Authentication**: JWT, Django Auth
- **File Storage**: Local storage (configurable for cloud storage)
- **Deployment**: Docker, Nginx, Gunicorn

## 📦 Installation

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mcart.git
   cd mcart
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database**
   ```bash
   python manage.py migrate
   python manage.py create_products_from_images
   python manage.py create_sample_blog_posts
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000` to see your site!

### Production Deployment

#### Option 1: Manual Deployment

1. **Prepare server** (Ubuntu/Debian)
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx
   ```

2. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/mcart.git
   cd mcart
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your production settings
   ```

4. **Setup database**
   ```bash
   sudo -u postgres createdb mcart_production
   sudo -u postgres createuser mcart_user
   # Set password and permissions
   ```

5. **Deploy**
   ```bash
   python manage.py migrate --settings=MCart.settings_production
   python manage.py setup_production --settings=MCart.settings_production
   python manage.py collectstatic --noinput --settings=MCart.settings_production
   ```

6. **Configure Gunicorn and Nginx** (see deploy.sh for details)

#### Option 2: Docker Deployment

1. **Using Docker Compose**
   ```bash
   docker-compose up -d
   ```

#### Option 3: Automated Deployment

1. **Run deployment script**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
SECRET_KEY=your-super-secret-key
DEBUG=False
DB_NAME=mcart_production
DB_USER=mcart_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Email Configuration

For production, configure SMTP settings in your environment variables:
- Gmail: Use app passwords
- SendGrid: Use API key
- AWS SES: Configure AWS credentials

### Payment Integration

To add payment gateways:
1. Install payment gateway SDK
2. Add payment models
3. Create payment views
4. Update checkout process

Popular options:
- Razorpay (India)
- Stripe (Global)
- PayPal (Global)

## 📱 API Documentation

The platform includes a complete REST API:

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/profile/` - User profile

### Product Endpoints
- `GET /products/` - List products
- `GET /product/{id}/` - Product details
- `GET /categories/` - List categories

### Cart & Orders
- `GET /cart/` - View cart
- `POST /cart/add/{product_id}/` - Add to cart
- `POST /checkout/` - Checkout process
- `GET /orders/` - Order history

## 🎨 Customization

### Themes
- Modify `shop/templates/shop/basic.html` for layout changes
- Update CSS in `shop/static/shop/css/`
- Customize Bootstrap variables

### Adding Features
1. Create new Django apps for major features
2. Add models in `models.py`
3. Create views and templates
4. Update URLs
5. Add admin configuration

## 🔒 Security

### Production Security Checklist
- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS (SSL certificate)
- [ ] Secure database credentials
- [ ] Configure CSRF and XSS protection
- [ ] Set up proper file permissions
- [ ] Configure firewall
- [ ] Regular security updates

## 📊 Performance

### Optimization Tips
- Use PostgreSQL for production
- Configure Redis for caching
- Optimize images and static files
- Use CDN for static content
- Enable gzip compression
- Database query optimization

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

## 📈 Monitoring

### Logging
Logs are configured for production in `settings_production.py`
- Application logs: `logs/django.log`
- Error tracking: Configure Sentry (optional)

### Analytics
- Google Analytics integration
- Custom analytics dashboard
- Sales reporting

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Documentation: [Wiki](https://github.com/yourusername/mcart/wiki)
- Issues: [GitHub Issues](https://github.com/yourusername/mcart/issues)
- Email: support@mcart.com

## 🎯 Roadmap

- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Advanced inventory management
- [ ] Subscription products
- [ ] Affiliate program
- [ ] Advanced SEO features
- [ ] Social media integration

---

## 🌟 Star this Repository

If you find MCart useful, please give it a ⭐ on GitHub! It helps others discover this project.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support & Community

- 🐛 **Issues**: [GitHub Issues](https://github.com/Kanishk-Malav/MCart/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Kanishk-Malav/MCart/discussions)
- 📧 **Email**: malavkanishq2@gmail.com
- 🌐 **Website**: [MCart Demo](https://mcart-demo.herokuapp.com) *(coming soon)*

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Kanishk-Malav/MCart?style=social)
![GitHub forks](https://img.shields.io/github/forks/Kanishk-Malav/MCart?style=social)
![GitHub issues](https://img.shields.io/github/issues/Kanishk-Malav/MCart)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Kanishk-Malav/MCart)

---

**MCart** - Built with ❤️ using Django by [Kanishk Malav](https://github.com/Kanishk-Malav)