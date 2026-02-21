# LUXE — Django E-Commerce

A modern, full-featured e-commerce application built with Django. Features a luxury editorial dark aesthetic with gold accents, built entirely with vanilla CSS and Django templates — no frontend framework required.

## Features

- **Product catalog** with categories, search, filtering, sorting
- **Product detail pages** with image gallery, reviews, and related products
- **Session-based cart** (works without login)
- **Wishlist** for authenticated users
- **Checkout flow** with order confirmation
- **Order management** (admin can update statuses)
- **User authentication** — register, login, profile, order history
- **Django Admin** — manage products, orders, categories
- **Responsive design** — works on mobile, tablet, desktop
- **Sticky filter bar** with live search
- **Animated product cards** with add-to-cart hover overlay
- **Flash messages** with auto-dismiss
- **Scroll-triggered animations**

## Stack

| Layer | Tech |
|---|---|
| Backend | Django 4.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Styling | Custom CSS (CSS Variables, Grid, Flexbox) |
| Fonts | Cormorant Garamond + DM Sans |
| Images | Pillow |
| Auth | Django built-in |

## Quick Start

### 1. Install dependencies

```bash
pip install django pillow
```

### 2. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed sample data

```bash
python seed_data.py
```

This creates:
- Admin user: `admin` / `admin123`
- 6 categories (Apparel, Accessories, Footwear, Home, Watches, Bags)
- 16 sample products with prices, discounts, and metadata

### 4. Collect static files (optional for dev)

```bash
python manage.py collectstatic
```

### 5. Start the server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

Admin: http://localhost:8000/admin/

---

## Project Structure

```
django-ecommerce/
├── ecommerce/              # Django project config
│   ├── settings.py
│   └── urls.py
├── store/                  # Main app
│   ├── models.py           # Category, Product, Order, Review, Wishlist
│   ├── views.py            # All page views
│   ├── urls.py             # URL routing
│   ├── forms.py            # Review, Checkout, Registration forms
│   ├── admin.py            # Admin customization
│   ├── context_processors.py  # Cart count in all templates
│   └── templates/store/    # All HTML templates
├── templates/
│   └── base.html           # Base layout with navbar/footer
├── static/
│   ├── css/main.css        # All styles (~700 lines)
│   └── js/main.js          # Cart interactivity, animations
├── media/                  # User-uploaded files (product images)
├── seed_data.py            # Sample data loader
├── requirements.txt
└── manage.py
```

## URL Reference

| URL | View |
|---|---|
| `/` | Home page |
| `/products/` | Product catalog with filters |
| `/products/<slug>/` | Product detail |
| `/category/<slug>/` | Category page |
| `/cart/` | Shopping cart |
| `/checkout/` | Checkout form |
| `/orders/` | Order history |
| `/orders/<id>/` | Order detail |
| `/wishlist/` | Saved products |
| `/login/` | Sign in |
| `/register/` | Create account |
| `/profile/` | User profile |
| `/admin/` | Django admin |

## Adding Product Images

Upload images via Django Admin → Products → Edit product → Image field.

Supported: JPEG, PNG, WebP (Pillow handles all formats)

## Production Checklist

- Set `DEBUG = False` in settings.py
- Change `SECRET_KEY` to a secure random value
- Configure PostgreSQL: update `DATABASES` in settings.py
- Set `ALLOWED_HOSTS` to your domain
- Set up a proper file storage (S3, etc.) for media files
- Run `collectstatic` and serve `/static/` from nginx/CDN
- Add HTTPS (Let's Encrypt)

## Customization

### Colors
Edit the CSS variables at the top of `static/css/main.css`:
```css
:root {
  --accent: #c9a96e;     /* Gold accent */
  --bg: #0a0a08;         /* Dark background */
  /* ... */
}
```

### Fonts
Change the Google Fonts import in `templates/base.html`:
```html
<link href="https://fonts.googleapis.com/css2?family=YourFont...">
```

### Adding Payment (Stripe)
1. `pip install stripe`
2. Replace the demo checkout form with Stripe Elements
3. Handle webhooks for order confirmation
