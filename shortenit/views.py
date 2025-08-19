from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.db import IntegrityError # for handling unique constraint errors    
from django.contrib import messages
from .models import URL
from .forms import CustomizeURLForm
from .utils import make_qr_code
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from io import BytesIO
from django.utils import timezone
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Count
import base64
import random
import string
import qrcode
import json

def index_view(request):
    if request.method == 'POST':
        original_url = request.POST['original_url']
        short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        
        # Associate URL with user if logged in
        url_obj = URL.objects.create(
            original_url=original_url, 
            short_url=short_url,
            user=request.user if request.user.is_authenticated else None
        )
        return render(request, 'short_url.html', {'url_obj': url_obj})
    
    # Get statistics for the homepage
    total_urls = URL.objects.count()
    total_clicks = sum(url.click_count for url in URL.objects.all())
    active_users = URL.objects.filter(user__isnull=False).values('user').distinct().count()
    
    context = {
        'total_urls': total_urls,
        'total_clicks': total_clicks,
        'active_users': active_users,
    }
    return render(request, 'index.html', context)

def redirect_to_original(request, short_url):
    url_obj = get_object_or_404(URL, short_url=short_url)

    # If expiry_date is set and in the past, send to expired page
    if url_obj.expiry_date and timezone.now() > url_obj.expiry_date:
        return redirect('expired_url', short_url=short_url)
    
    url_obj.click_count += 1
    url_obj.save()
    return redirect(url_obj.original_url)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

@login_required
def dashboard_view(request):
    user_urls = URL.objects.filter(user=request.user).order_by('-creation_date')
    total_clicks = sum(url.click_count for url in user_urls)
    context = {
        'user_urls': user_urls,
        'total_urls': user_urls.count(),
        'total_clicks': total_clicks
    }
    return render(request, 'dashboard.html', context)

@login_required
def my_urls_view(request):
    user_urls = URL.objects.filter(user=request.user).order_by('-creation_date')
    return render(request, 'my_urls.html', {'user_urls': user_urls})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def customize_url_view(request, url_id):
    url_obj = get_object_or_404(URL, pk=url_id, user=request.user)

    if request.method == "POST":
        form = CustomizeURLForm(request.POST, instance=url_obj)
        if form.is_valid():
            try:
                # prepare the model instance but don't commit yet
                url = form.save(commit=False)

                # if user wants a fresh QR, build the absolute short link
                if form.cleaned_data.get("generate_qr"):
                    short_link = f"{request.scheme}://{request.get_host()}/{url.short_url}/"
                    qr_file = make_qr_code(short_link)
                    url.qr_code_image.save(qr_file.name, qr_file, save=False)

                # now persist both slug changes and (optional) QR image
                url.save()
                messages.success(request, "Your link has been updated!")
                return redirect("dashboard")

            except IntegrityError:
                form.add_error(
                    "short_url",
                    "That custom slug is already taken. Please choose another."
                )
    else:
        form = CustomizeURLForm(instance=url_obj)

    return render(request, "customize_url.html", {
        "form": form,
        "url_obj": url_obj,
    })

@login_required
@require_POST
def preview_qr(request):
    slug = request.POST.get("slug", "").strip()
    if not slug:
        return JsonResponse({"error": "Slug cannot be empty."}, status=400)

    # Build your full short link
    short_link = f"{request.scheme}://{request.get_host()}/{slug}/"

    # Generate a PIL.Image QR
    img = qrcode.make(short_link)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    data_uri = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({
        "short_link": short_link,
        "qr_data_uri": data_uri,
    })

@login_required
@require_POST
def update_slug(request, pk):
    """
    Inline AJAX handler to rename a slug.
    Supports both JSON bodies and form-encoded POSTs.
    """
    url_obj = get_object_or_404(URL, pk=pk, user=request.user)

    # 1) Try to parse JSON payload
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, TypeError):
        # fallback to form data if JSON parsing fails
        payload = request.POST

    # 2) Extract & clean the new slug
    new_slug = payload.get("short_url", "").strip()
    if not new_slug:
        return JsonResponse({"error": "Slug cannot be blank."}, status=400)

    # 3) Enforce uniqueness
    conflict = URL.objects.exclude(pk=pk).filter(short_url=new_slug).exists()
    if conflict:
        return JsonResponse({"error": "That slug is already taken."}, status=400)

    # 4) Save and respond
    url_obj.short_url = new_slug
    url_obj.save()
    return JsonResponse({"success": True, "short_url": new_slug})


@login_required
@require_POST
def delete_url(request, pk):
    """
    AJAX handler to delete a URL.
    """
    url_obj = get_object_or_404(URL, pk=pk, user=request.user)
    url_obj.delete()
    return JsonResponse({"success": True})

def expired_url(request, short_url):
    """
    Renders a friendly page when a link has passed its expiry_date.
    Returns HTTP 410 Gone.
    """
    context = {'short_url': short_url}
    return render(request, 'expired_url.html', context, status=410)

@login_required
def analytics_view(request):
    # 1. Search
    q = request.GET.get('q', '').strip()
    urls = URL.objects.all().order_by('-creation_date')
    if q:
        urls = urls.filter(
            Q(short_url__icontains=q) |
            Q(original_url__icontains=q)
        )

    # 2. Prepare Chart Data: URLs per category
    category_data = (
        URL.objects
           .values('category')
           .annotate(count=Count('id'))
           .order_by('category')
    )
    labels = [item['category'].title() for item in category_data]
    data = [item['count'] for item in category_data]

    context = {
        'urls': urls,
        'search_query': q,
        'chart_labels': json.dumps(labels),
        'chart_data':  json.dumps(data),
    }
    return render(request, 'analytics.html', context)
