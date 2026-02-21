"""
Run this after migrations to populate sample data:
    python manage.py shell < seed_data.py
Or:
    python seed_data.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from store.models import Category, Product
from django.contrib.auth.models import User

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@luxe.com', 'admin123')
    print("✓ Superuser created: admin / admin123")

# Categories
cats = [
    ('Apparel', 'apparel', 'Premium clothing and outerwear'),
    ('Accessories', 'accessories', 'Curated accessories and jewelry'),
    ('Footwear', 'footwear', 'Designer shoes and boots'),
    ('Home', 'home', 'Luxury home goods'),
    ('Watches', 'watches', 'Fine timepieces'),
    ('Bags', 'bags', 'Leather goods and bags'),
]
cat_objects = {}
for name, slug, desc in cats:
    cat, created = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
    cat_objects[slug] = cat
    if created:
        print(f"✓ Category: {name}")

# Products
products = [
    # Apparel
    ('Merino Wool Turtleneck', 'merino-wool-turtleneck', 'apparel', 245.00, 320.00, 50, True, True),
    ('Cashmere Overshirt', 'cashmere-overshirt', 'apparel', 380.00, None, 30, True, False),
    ('Slim Trench Coat', 'slim-trench-coat', 'apparel', 590.00, 740.00, 20, True, False),
    ('Oxford Button-Down', 'oxford-button-down', 'apparel', 145.00, None, 80, False, True),
    # Accessories
    ('Woven Leather Belt', 'woven-leather-belt', 'accessories', 120.00, None, 60, False, True),
    ('Silk Pocket Square', 'silk-pocket-square', 'accessories', 65.00, None, 100, False, False),
    ('Tortoise Sunglasses', 'tortoise-sunglasses', 'accessories', 280.00, 340.00, 40, True, True),
    # Footwear
    ('Derby Leather Shoes', 'derby-leather-shoes', 'footwear', 420.00, None, 35, True, False),
    ('Chelsea Boots', 'chelsea-boots', 'footwear', 495.00, 580.00, 25, True, True),
    ('Canvas Sneakers', 'canvas-sneakers', 'footwear', 185.00, None, 70, False, True),
    # Home
    ('Linen Throw Blanket', 'linen-throw-blanket', 'home', 195.00, None, 45, False, True),
    ('Ceramic Coffee Set', 'ceramic-coffee-set', 'home', 145.00, 180.00, 30, True, False),
    # Watches
    ('Minimalist Field Watch', 'minimalist-field-watch', 'watches', 850.00, None, 15, True, False),
    ('Dive Watch 200m', 'dive-watch-200m', 'watches', 1250.00, 1600.00, 8, True, True),
    # Bags
    ('Waxed Canvas Tote', 'waxed-canvas-tote', 'bags', 225.00, None, 40, False, True),
    ('Bridle Leather Briefcase', 'bridle-leather-briefcase', 'bags', 680.00, 820.00, 12, True, False),
]

DESCRIPTIONS = {
    'apparel': 'Expertly crafted from premium natural fibers, this piece combines timeless silhouette with modern sensibility. The fit is considered and refined, designed to be worn season after season.',
    'accessories': 'A refined accent for the discerning wardrobe. Handcrafted from the finest materials by skilled artisans, each detail has been considered with care.',
    'footwear': 'Constructed using traditional techniques with full-grain leather uppers and leather-lined insoles. Built to develop a rich patina with wear.',
    'home': 'Thoughtfully made to elevate your everyday rituals. Natural materials, considered design, and lasting quality define this piece.',
    'watches': 'A precision timepiece for those who value craft. Swiss movement, sapphire crystal, and meticulous finishing throughout.',
    'bags': 'Vegetable-tanned leather that ages beautifully with use. Every seam is hand-stitched, every edge burnished by hand.',
}

for name, slug, cat_slug, price, compare, stock, featured, is_new in products:
    cat = cat_objects[cat_slug]
    prod, created = Product.objects.get_or_create(
        slug=slug,
        defaults={
            'name': name,
            'category': cat,
            'price': price,
            'compare_price': compare,
            'stock': stock,
            'is_featured': featured,
            'is_new': is_new,
            'description': DESCRIPTIONS.get(cat_slug, 'A premium product of exceptional quality.'),
        }
    )
    if created:
        print(f"✓ Product: {name}")

print("\n✅ Seed complete!")
print("   Admin: http://localhost:8000/admin/ (admin / admin123)")
print("   Site:  http://localhost:8000/")
