from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import URL

def validate_http_https(value):
    """
    Ensures the URL starts with http:// or https://
    """
    validator = URLValidator(schemes=['http', 'https'])
    try:
        validator(value)
    except ValidationError:
        raise ValidationError(
            'Please enter a valid URL starting with http:// or https://',
            code='invalid_scheme'
        )

class URLForm(forms.ModelForm):
    original_url = forms.URLField(
        max_length=200,
        validators=[validate_http_https],
        widget=forms.URLInput(attrs={
            'id': 'original_url',
            'placeholder': 'https://example.com',
            'class': 'form-control'
        }),
        error_messages={
            'invalid': 'Please enter a valid URL starting with http:// or https://'
        },
        help_text='URL must start with http:// or https://'
    )

    class Meta:
        model = URL
        fields = ['original_url']

class CustomizeURLForm(forms.ModelForm):
    generate_qr = forms.BooleanField(
        required=False,
        help_text="Check to generate/update the QR code for this link"
    )

    class Meta:
        model = URL
        fields = [
            "short_url",
            "expiry_date",
            "category",
        ]
        widgets = {
            "expiry_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }