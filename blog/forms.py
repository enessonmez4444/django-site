from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['isim', 'email', 'konu', 'mesaj']
        widgets = {
            'isim': forms.TextInput(attrs={'placeholder': 'Adınız', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-posta adresiniz', 'class': 'form-input'}),
            'konu': forms.TextInput(attrs={'placeholder': 'Konu', 'class': 'form-input'}),
            'mesaj': forms.Textarea(attrs={'placeholder': 'Mesajınız', 'class': 'form-textarea', 'rows':5}),
        }