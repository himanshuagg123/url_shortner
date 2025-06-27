# url_shortener/urls.py (project-level)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shortener.urls')),  # <-- This must be here without a prefix
]
