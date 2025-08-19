from django.contrib import admin
from .models import URL

class URLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_url', 'click_count', 'creation_date')

admin.site.register(URL, URLAdmin)


