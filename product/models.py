from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)  # The name of the category (e.g., "Spices", "Beverages").
    description = models.TextField(null=True, blank=True)  # A short description about the category.
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)  # Optional image for the category.
    slug = models.SlugField(unique=True)  # A unique slug to be used in the URL for the category.
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the category was created.

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()  # A detailed description of the product.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product.
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # Main image for the product.
    image_2 = models.ImageField(upload_to='products/', null=True, blank=True)  # Second image for the product.
    image_3 = models.ImageField(upload_to='products/', null=True, blank=True)  # Third image for the product.
    image_4 = models.ImageField(upload_to='products/', null=True, blank=True)  # Fourth image for the product.
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)  # Related category.
    stock = models.IntegerField(default=0)  # The quantity of the product in stock.
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional weight of the product (for shipping calculations).
    is_active = models.BooleanField(default=True)  # Whether the product is currently available for purchase.
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the product was added.
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the product was last updated.

    def __str__(self):
        return self.name
