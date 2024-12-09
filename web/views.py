from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django import forms

from .models import *
from custemer.models import *
from product.models import *

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password

User = get_user_model()
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from product.models import *
from django.db.models import Q




def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    cart_items = Cart.objects.filter(customer__user=request.user)

    # Create a dictionary to store the cart items for each product
    for product in products:
        cart_item = cart_items.filter(product=product).first()  # Get the first cart item for the product, or None
        product_in_cart = cart_item is not None

        # Attach the `product_in_cart` and `cart_item` to each product
        product.product_in_cart = product_in_cart
        product.cart_item = cart_item

    context = {
        'categories': categories,
        'cart_items': cart_items,
        'products': products,
    }
    return render(request, 'web/index.html', context=context)




@login_required  
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item = Cart.objects.filter(customer__user=request.user, product=product).first()

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]

    star_range = [1, 2, 3, 4, 5]

    context = {
        'product': product,
        'related_products': related_products,
        'star_range': star_range,
        'cart_item': cart_item,
        'product_in_cart': bool(cart_item),
    }

    return render(request, 'web/product_detail.html', context)



def add_cart(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    product = Product.objects.get(id=id)

    cart = Cart.objects.create(
        customer=customer,
        product=product,
        amouunt=product.price,
        quantity=1
    )
    
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def cart_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    customer = get_object_or_404(Customer, user=request.user)
    cart_items = Cart.objects.filter(customer=customer)
    total_price = sum(item.amouunt for item in cart_items)
    
    return render(request, 'web/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })



def update_cart_quantity(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart_item = get_object_or_404(Cart, id=id, customer__user=request.user)

    action = request.POST.get('action')
    if action == "increase":
        cart_item.quantity += 1
        cart_item.amouunt = cart_item.quantity * cart_item.product.price
        cart_item.save()
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.amouunt = cart_item.quantity * cart_item.product.price
            cart_item.save()
        else:
            cart_item.delete()
            messages.info(request, "Item removed from the cart.")

    messages.success(request, "Cart updated successfully.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def remove_cart_item(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_item = get_object_or_404(Cart, id=id, customer__user=request.user)
    cart_item.delete()

    messages.success(request, "Item removed from the cart.")
    return redirect('web:cart_page')




@login_required
def checkout(request):
    cart_items = Cart.objects.filter(customer__user=request.user)
    cart_total = sum(item.quantity * item.product.price for item in cart_items)

   
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    return render(request, 'web/checkout.html', context)


@login_required
def order_confirmation(request, id):
    order = get_object_or_404(Order, id=id, customer__user=request.user)
    formatted_payment_method = order.payment_method.replace('_', ' ').capitalize()
    oitem = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'oitem': oitem,
        'formatted_payment_method': formatted_payment_method,
    }
    return render(request, 'web/order_confirmation.html', context)



@login_required
def place_order(request):
    try:
        user = request.user
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found. Please update your profile.")
        return redirect('web:update_profile')

    cart_items = Cart.objects.filter(customer=customer)
    cart_total = sum(item.quantity * item.product.price for item in cart_items)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('web:cart')

    if request.method == 'POST':
        address = request.POST.get('address')
        full_name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        place = request.POST.get('place')
        pincode = request.POST.get('pin')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        if not address or not payment_method:
            messages.error(request, "Please provide a delivery address and select a payment method.")
            return redirect('web:checkout')

        order = Order.objects.create(
            customer=customer,
            full_name=full_name,
            mobile_number=mobile_number,
            place=place,
            pincode=pincode,
            total=cart_total,
            address=address,
            payment_method=payment_method,
            status='Pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.amouunt
            )
            item.delete() 

        messages.success(request, "Your order has been placed successfully!")
        return redirect('web:order_confirmation', order.id)

    return redirect('web:checkout')



@login_required
def track_order(request, order_id):
    # Ensure the order belongs to the logged-in user
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)

    # Fetch all items associated with the order
    order_items = OrderItem.objects.filter(order=order)

    # Extract the status choices for rendering the progress bar
    status_choices = list(Order.STATUS_CHOICES)  # Convert to list for easier manipulation
    current_status_index = next(
        (index for index, status in enumerate(status_choices) if status[0] == order.status),
        -1
    )

    return render(request, 'web/track_order.html', {
        'order': order,
        'order_items': order_items,
        'status_choices': status_choices,
        'current_status_index': current_status_index,
    })


@login_required
def all_orders(request):
    orders = Order.objects.filter(customer__user=request.user).order_by('-created_at')

    return render(request, 'web/all_orders.html', {'orders': orders})



def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(price__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if category_filter:
        products = products.filter(category__id=category_filter)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        'categories': categories,
        'products': products,
        'search_query': search_query,
        'category_filter': category_filter,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'web/product_list.html', context)
