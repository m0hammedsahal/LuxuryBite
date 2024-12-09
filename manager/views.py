from main.decorators import allow_manager

from main.functions import generate_form_errors


# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.contrib.auth.decorators import login_required
from users.models import User
from custemer.models import *


from web.models import *


from django.contrib.auth import logout as auth_logout

from django.contrib import messages
from .forms import *
 # Ensure only logged-in users can access the index view


@login_required(login_url='manager:login')
@allow_manager
def index(request):
    
    return render(request, 'manager/index.html')



def unauthorized_access(request):
    
    return render(request, 'manager/unauthorized_access.html')



# store_category_list

def category_list(request):
    instances = Category.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/category_list.html', context=context)




def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('manager:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()

    return render(request, 'manager/category_form.html', {'form': form})


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('web:category_list')

    return render(request, 'category_confirm_delete.html', {'category': category})



def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('web:category_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category_form.html', {'form': form, 'category': category})




# product_list

def product_list(request):
    instances = Product.objects.all()

    context = {
            "instances": instances,
            
    }
    return render(request, 'manager/product_list.html', context=context)




def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manager:product_list')  # Adjust the redirect to your desired URL
    else:
        form = ProductForm()
    return render(request, 'manager/product_form.html', {'form': form})

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manager:product_list')  # Adjust the redirect
    else:
        form = ProductForm(instance=product)
    return render(request, 'manager/product_form.html', {'form': form})

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    product.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



# product_list

def orders_list(request):
    instances = Order.objects.all()
    instances_items = OrderItem.objects.all()

    context = {
            "instances": instances,
            "instances_items": instances_items,
            
    }
    return render(request, 'manager/orders_list.html', context=context)




def order_track(request, id):
    instance = Order.objects.get(id=id)
    if instance.status == 'Pending':
        instance.status = 'Preparing'
        instance.save()

    elif instance.status == 'Preparing':
        instance.status = 'Ready for Pickup/Delivery'
        instance.save()
        
    elif instance.status == 'Ready for Pickup/Delivery':
        instance.status = 'Dispatched'
        instance.save()
        
    elif instance.status == 'Dispatched':
        instance.status = 'Delivered'
        instance.save()
    
    
    # return render(request, 'manager/forms/order_track.html', context=context)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cancel_order(request, id):
    instance = Order.objects.get(id=id)

    if instance.status != 'Cancelled':
        instance.status = 'Cancelled'
        instance.save()
        messages.success(request, "Order has been cancelled.")
    else:
        messages.warning(request, "This order is already cancelled.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))