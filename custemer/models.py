from django.db import models
from users.models import User
from product.models import *

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'users_customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ['-id']
    
    def __str__(self):
        return self.user.email



class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amouunt = models.FloatField()
    quantity = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customer_cart'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ['-id']
    
    def __str__(self):
        return self.customer.user.email
    



class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Ready for Pickup/Delivery', 'Ready for Pickup/Delivery'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)

    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # New field
    offer_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)


    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField()
    place = models.TextField()

    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash_on_delivery', 'Cash on Delivery')
    ])
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customer_order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['-id']
    
    def __str__(self):
        return self.customer.user.email
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'customer_orderitem'
        verbose_name = 'orderitem'
        verbose_name_plural = 'orderitems'
        ordering = ['-id']
    
    def __str__(self):
        return self.order.customer.user.email