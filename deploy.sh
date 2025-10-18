#!/bin/bash

# MCart Deployment Script

echo "🚀 Starting MCart deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system packages
echo "🔧 Installing system dependencies..."
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Setup PostgreSQL database
echo "🗄️ Setting up database..."
sudo -u postgres createdb mcart_production
sudo -u postgres createuser mcart_user
sudo -u postgres psql -c "ALTER USER mcart_user WITH PASSWORD 'your-secure-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE mcart_production TO mcart_user;"

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate --settings=MCart.settings_production

# Create superuser
echo "👤 Setting up admin user..."
python manage.py setup_production --settings=MCart.settings_production

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=MCart.settings_production

# Setup Gunicorn service
echo "⚙️ Setting up Gunicorn service..."
sudo tee /etc/systemd/system/mcart.service > /dev/null <<EOF
[Unit]
Description=MCart Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/venv/bin"
ExecStart=/path/to/your/project/venv/bin/gunicorn --workers 3 --bind unix:/path/to/your/project/mcart.sock MCart.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start and enable Gunicorn service
sudo systemctl start mcart
sudo systemctl enable mcart

# Setup Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/mcart > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project;
    }
    
    location /media/ {
        root /path/to/your/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/your/project/mcart.sock;
    }
}
EOF

# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/mcart /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt (optional)
echo "🔒 Setting up SSL certificate..."
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

echo "✅ MCart deployment completed successfully!"
echo "🌐 Your site should now be available at https://your-domain.com"