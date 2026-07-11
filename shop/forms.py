from django import forms
from .models import Seller, Product

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['store_name', 'store_description', 'address', 'phone']
        widgets = {
            'store_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your store name'
            }),
            'store_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your store...'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your business address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required
        for field in self.fields:
            self.fields[field].required = True


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        exclude = (
            "seller",
            "created_at",
            "updated_at",
            "rating",
        )

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),
            "short_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "discount_price": forms.NumberInput(attrs={"class": "form-control"}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control"}),
            "weight": forms.NumberInput(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "main_image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "meta_title": forms.TextInput(attrs={"class": "form-control"}),
            "meta_description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2
            }),
            "tags": forms.SelectMultiple(attrs={
                "class": "form-select"
            }),
        }

    def clean(self):

        cleaned_data = super().clean()

        price = cleaned_data.get("price")
        discount = cleaned_data.get("discount_price")
        stock = cleaned_data.get("stock")

        if discount and price and discount >= price:
            self.add_error(
                "discount_price",
                "Discount price must be less than actual price."
            )

        if stock is not None and stock < 0:
            self.add_error(
                "stock",
                "Stock cannot be negative."
            )

        return cleaned_data