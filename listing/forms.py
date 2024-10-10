from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'realtor', 'title', 'slug', 'address', 'city', 'region', 'zipcode',
            'description', 'price', 'bedrooms', 'sqft', 'lot_size', 'parking_space',
            'bathrooms', 'sale_type', 'home_type', 'main_photo', 'photo_1', 'photo_2',
            'photo_3', 'photo_4', 'photo_5', 'photo_6', 'photo_7', 'photo_8', 'photo_9',
            'photo_10', 'video_files', 'is_published'
        ]
        widgets = {
            'realtor': forms.EmailInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'sqft': forms.NumberInput(attrs={'class': 'form-control'}),
            'lot_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'parking_space': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'sale_type': forms.Select(attrs={'class': 'form-control'}),
            'home_type': forms.Select(attrs={'class': 'form-control'}),
            'main_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_6': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_7': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_8': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_9': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_10': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video_files': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }