from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from .models import Profile

class VerifiedEmailPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        users = User._default_manager.filter(email__iexact=email, is_active=True)

        verified_ids = Profile.objects.filter(
            user__in=users,
            email_verified=True
        ).values_list("user_id", flat=True)

        return users.filter(id__in=verified_ids)

from django import forms
from django.contrib.auth.models import User
from .models import Profile, Document

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo"]
        widgets = {
            "photo": forms.ClearableFileInput(attrs={"class": "input"})
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input", "placeholder": "Seu nome"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "seu@email.com"}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["category", "title", "description", "external_url", "file"]
        widgets = {
            "category": forms.Select(attrs={"class": "input"}),
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "Título"}),
            "description": forms.Textarea(attrs={"class": "input", "rows": 3, "placeholder": "Descrição (opcional)"}),
            "external_url": forms.URLInput(attrs={"class": "input", "placeholder": "https://... (opcional)"}),
            "file": forms.ClearableFileInput(attrs={"class": "input"}),
        }
