from django import forms
from web.models import *
from custemer.models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter a brief description of the category (optional)'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a unique slug for the category'
            }),
        }
        labels = {
            'name': 'Category Name',
            'description': 'Description',
            'image': 'Category Image',
            'slug': 'Slug (Unique URL Identifier)',
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Category.objects.filter(slug=slug).exists():
            raise forms.ValidationError('The slug must be unique. This one already exists.')
        return slug




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 
            'description', 
            'price', 
            'image', 
            'image_2', 
            'image_3', 
            'image_4', 
            'category', 
            'stock', 
            'weight', 
            'is_active'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Quantity'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (optional)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
