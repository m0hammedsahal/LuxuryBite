# Generated by Django 5.1.1 on 2024-12-09 05:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
                'db_table': 'users_customer',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('delivery_charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('offer_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.TextField()),
                ('place', models.TextField()),
                ('payment_method', models.CharField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash_on_delivery', 'Cash on Delivery')], max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Preparing', 'Preparing'), ('Ready for Pickup/Delivery', 'Ready for Pickup/Delivery'), ('Dispatched', 'Dispatched'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'db_table': 'customer_order',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'orderitem',
                'verbose_name_plural': 'orderitems',
                'db_table': 'customer_orderitem',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amouunt', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
                'db_table': 'customer_cart',
                'ordering': ['-id'],
            },
        ),
    ]
