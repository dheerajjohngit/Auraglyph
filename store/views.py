
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from decimal import Decimal

from .models import Product, Wishlist, Cart, Order, OrderItem


# -------------------------
# HOME AND STATIC PAGES
# -------------------------

def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def phones(request):
    return render(request, 'phones.html')


def accessories(request):
    return render(request, 'accessories.html')


def audio(request):
    return render(request, 'audio.html')


def watch(request):
    return render(request, 'watch.html')


def cmf(request):
    return render(request, 'cmf.html')


# -------------------------
# PRODUCT DETAILS
# -------------------------

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    # Import recommendations only when product details are requested.
    from .recommendation import get_recommendations

    recommended_products = get_recommendations(product.id)

    return render(
        request,
        'product-detail.html',
        {
            'product': product,
            'recommended_products': recommended_products,
        }
    )


# -------------------------
# WISHLIST
# -------------------------

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)

    return render(
        request,
        'wishlist.html',
        {'wishlist_items': wishlist_items}
    )


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('/wishlist/#wishlist-products')


@login_required
def remove_from_wishlist(request, id):
    item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect('/wishlist/#wishlist-products')


# -------------------------
# CART
# -------------------------

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart/#cart-section')


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect('/cart/#cart-section')


# -------------------------
# CHECKOUT
# -------------------------

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    subtotal = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    gst = subtotal * Decimal('0.18')
    total = subtotal + gst

    if request.method == "POST":

        if not cart_items.exists():
            return redirect('home')

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode'],
            payment_method=request.POST['payment_method'],
            total_amount=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        cart_items.delete()

        return redirect('home')

    return render(
        request,
        'checkout.html',
        {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'gst': gst,
            'total': total,
        }
    )


@login_required
def buy_now(request, id):
    product = get_object_or_404(Product, id=id)

    Cart.objects.filter(user=request.user).delete()

    Cart.objects.create(
        user=request.user,
        product=product,
        quantity=1
    )

    return redirect('/checkout/#checkout-section')


# -------------------------
# USER REGISTRATION
# -------------------------

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'register.html',
                {'error': 'Username already exists'}
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')


# -------------------------
# USER LOGIN
# -------------------------

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# -------------------------
# USER LOGOUT
# -------------------------

def logout_user(request):
    logout(request)
    return redirect('home')


# -------------------------
# USER ORDERS
# -------------------------

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders.html',
        {'orders': orders}
    )


# -------------------------
# ANALYTICS DASHBOARD
# -------------------------

@login_required
def analytics_dashboard(request):

    # Load ML modules only when the analytics page is opened.
    from .customer_segmentation import get_customer_segments
    from .sales_forecasting import predict_next_month_sales
    from .value_for_money import calculate_vfm, predict_vfm

    total_users = User.objects.count()
    total_orders = Order.objects.count()

    total_revenue = Order.objects.aggregate(
        revenue=Sum('total_amount')
    )['revenue'] or 0

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0 else 0
    )

    segments = get_customer_segments()

    category_data = {}

    for category, display_name in Product.CATEGORY_CHOICES:
        total_sold = (
            OrderItem.objects
            .filter(product__category=category)
            .aggregate(total=Sum('quantity'))
        )['total'] or 0

        category_data[display_name] = total_sold

    monthly_revenue = (
        Order.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('total_amount'))
        .order_by('month')
    )

    revenue_labels = []
    revenue_values = []

    for item in monthly_revenue:
        revenue_labels.append(
            item['month'].strftime('%b %Y')
        )

        revenue_values.append(
            float(item['total'])
        )

    forecasted_sales = predict_next_month_sales(
        revenue_values
    )

    top_products = (
        OrderItem.objects
        .values('product__name')
        .annotate(total_sales=Sum('quantity'))
        .order_by('-total_sales')[:5]
    )

    products = Product.objects.all()
    vfm_products = []

    for product in products:
        score = calculate_vfm(product)
        prediction = predict_vfm(score)

        vfm_products.append({
            'name': product.name,
            'score': score,
            'prediction': prediction,
        })

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'category_data': category_data,
        'top_products': top_products,
        'vfm_products': vfm_products,
        'forecasted_sales': forecasted_sales,
        'chart_labels': list(category_data.keys()),
        'chart_values': list(category_data.values()),
        'revenue_labels': revenue_labels,
        'revenue_values': revenue_values,
        'total_revenue': f"{float(total_revenue):,.2f}",
        'average_order_value': f"{float(average_order_value):,.2f}",
        'high_value_customers': segments['high_value'],
        'regular_customers': segments['regular'],
        'new_customers': segments['new'],
    }

    return render(
        request,
        'analytics.html',
        context
    )
