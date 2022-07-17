from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter admin email",
            }
        ),
        required=True,
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control password-box",
                "placeholder": "Enter your password",
            }
        ),
        required=True,
    )
