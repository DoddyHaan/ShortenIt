from django import forms
from .models import URL

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