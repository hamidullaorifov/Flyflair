from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(),
    )
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    allowed_domains = ["flyflair.com"]

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        domain = email.split("@")[-1]
        if domain not in self.allowed_domains:
            raise ValidationError("You must register with a flair domain")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")

        return email



    def clean(self):
        # Using this to ensure extra validations are in place.
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        # Password Validation
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error("password", " ".join(e.messages))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_domains = ["flyflair.com"]





