from django.db import models
from django.contrib.auth.models import User
from django.conf import settings # for get_full_short_url helper
from django.utils import timezone


class URL(models.Model):
    CATEGORY_CHOICES = [
        ('work',    'Work'),
        ('socials', 'Socials'),
        ('other',   'Other'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    original_url = models.URLField(max_length=200)
    short_url = models.SlugField(
        max_length=50, unique=True,
        help_text="Customize the slug portion of your link"
    )
    click_count = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)

    # Customization fields
    expiry_date = models.DateTimeField(null=True, blank=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        blank=True
    )
    qr_code_image = models.ImageField(
        upload_to="qr_codes/", null=True, blank=True
    )

    def __str__(self):
        return self.original_url
    
    @property
    def is_expired(self):
        if self.expiry_date:
            return timezone.now() > self.expiry_date
        return False


