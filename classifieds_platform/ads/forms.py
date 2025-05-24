from django import forms
from .models import Ad, Category,Message,Report


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'location', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter keywords'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label='All Categories', widget=forms.Select(attrs={'class': 'form-control'}))
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Min Price', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}))
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Max Price', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1000.00'}))
    location = forms.CharField(max_length=200, required=False, label='Location', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City or area'}))
    sort_by = forms.ChoiceField(
        choices=[
            ('created_at', 'Newest First'),
            ('-created_at', 'Oldest First'),
            ('price', 'Price: Low to High'),
            ('-price', 'Price: High to Low'),
        ],
        required=False,
        label='Sort By',
        widget=forms.Select(attrs={'class': 'form-control'})
    )



class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Explain why you are reporting this ad'}),
        }
