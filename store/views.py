from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Order, OrderItem, Review, Wishlist
from .forms import ReviewForm, CheckoutForm, UserRegistrationForm
import json


# ── Cart helpers (session-based) ──────────────────────────────────────────────

def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def cart_total(cart, products):
    total = 0
    for pid, qty in cart.items():
        p = products.get(int(pid))
        if p:
            total += p.price * qty
    return total


# ── Pages ─────────────────────────────────────────────────────────────────────

def home(request):
    featured = Product.objects.filter(is_featured=True, stock__gt=0)[:8]
    new_arrivals = Product.objects.filter(is_new=True, stock__gt=0)[:8]
    categories = Category.objects.all()[:6]
    return render(request, 'store/home.html', {
        'featured': featured,
        'new_arrivals': new_arrivals,
        'categories': categories,
    })


def product_list(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()

    cat_slug = request.GET.get('category')
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'newest')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if cat_slug:
        products = products.filter(category__slug=cat_slug)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort_map = {
        'newest': '-created_at',
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
    }
    products = products.order_by(sort_map.get(sort, '-created_at'))

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': cat_slug,
        'query': query,
        'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.select_related('user').order_by('-created_at')
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    review_form = ReviewForm()

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            rev = review_form.save(commit=False)
            rev.product = product
            rev.user = request.user
            rev.save()
            messages.success(request, 'Review submitted!')
            return redirect('store:product_detail', slug=slug)

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related': related,
        'review_form': review_form,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, stock__gt=0)
    return render(request, 'store/category.html', {'category': category, 'products': products})


# ── Cart ──────────────────────────────────────────────────────────────────────

def cart_view(request):
    cart = get_cart(request)
    products = {}
    if cart:
        qs = Product.objects.filter(id__in=[int(k) for k in cart.keys()])
        products = {p.id: p for p in qs}
    total = cart_total(cart, products)
    return render(request, 'store/cart.html', {'cart': cart, 'products': products, 'total': total})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    pid = str(product_id)
    qty = int(request.POST.get('quantity', 1))
    cart[pid] = cart.get(pid, 0) + qty
    save_cart(request, cart)
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'store:cart'))


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    save_cart(request, cart)
    return redirect('store:cart')


def update_cart(request, product_id):
    cart = get_cart(request)
    qty = int(request.POST.get('quantity', 1))
    if qty <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = qty
    save_cart(request, cart)
    return redirect('store:cart')


# ── Checkout & Orders ─────────────────────────────────────────────────────────

@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart:
        return redirect('store:cart')
    products = {p.id: p for p in Product.objects.filter(id__in=[int(k) for k in cart.keys()])}
    total = cart_total(cart, products)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_price=total,
                shipping_name=form.cleaned_data['name'],
                shipping_address=form.cleaned_data['address'],
                shipping_city=form.cleaned_data['city'],
                shipping_zip=form.cleaned_data['zip_code'],
            )
            for pid, qty in cart.items():
                p = products.get(int(pid))
                if p:
                    OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
                    p.stock -= qty
                    p.save()
            request.session['cart'] = {}
            messages.success(request, 'Order placed successfully!')
            return redirect('store:order_detail', pk=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {'form': form, 'cart': cart, 'products': products, 'total': total})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


# ── Wishlist ──────────────────────────────────────────────────────────────────

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'items': items})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
        messages.info(request, f'Removed from wishlist.')
    else:
        messages.success(request, f'Added to wishlist!')
    return redirect(request.META.get('HTTP_REFERER', 'store:wishlist'))


# ── Auth ──────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(request.GET.get('next', 'store:home'))
    return render(request, 'store/login.html', {'form': form})


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created! Welcome!')
        return redirect('store:home')
    return render(request, 'store/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('store:home')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'store/profile.html', {'orders': orders})
