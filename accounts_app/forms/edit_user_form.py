from django import forms

from accounts_app.models import User


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "occupation"]

        widgets = {
            "occupation": forms.TextInput(attrs={"maxlength": 15, "class": "form-input"}),
            "first_name": forms.TextInput(attrs={"class": "form-input"}),
            "last_name": forms.TextInput(attrs={"class": "form-input"}),
        }
        help_texts = {
            "occupation": "Short (max 15 characters).",
        }
