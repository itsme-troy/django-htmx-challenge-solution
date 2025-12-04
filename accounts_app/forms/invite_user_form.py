from django import forms


class InviteUserForm(forms.Form):
    # create email input field
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg "
                     "focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary",
            "placeholder": "user@example.com"
        })
    )