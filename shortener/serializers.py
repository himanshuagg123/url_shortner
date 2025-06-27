# shortener/serializers.py

from rest_framework import serializers
from .models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ['code', 'long_url', 'expires_at', 'created_at']
        read_only_fields = ['code', 'created_at']
