from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my-urls/', views.my_urls_view, name='my_urls'),
    path('profile/', views.profile_view, name='profile'),
    path('preview-qr/', views.preview_qr, name='preview_qr'),
    path('customize/<int:url_id>/',views.customize_url_view,name='customize_url'),
    path('update-slug/<int:pk>/', views.update_slug, name='update_slug'),
    path('delete-url/<int:pk>/', views.delete_url, name='delete_url'),
    path('expired/<str:short_url>/', views.expired_url, name='expired_url'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('<str:short_url>/', views.redirect_to_original, name='short_url'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

