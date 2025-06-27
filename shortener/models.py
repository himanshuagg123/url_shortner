from django.db import models
from django.utils import timezone
from django.conf import settings
from .random import generate_unique_code


class ShortenedURL(models.Model):
    """
    Stores the mapping between a long URL and its shortened version.
    """

    long_url = models.URLField(help_text="Enter the original long URL.")
    code = models.CharField(
        max_length=10,
        unique=True,
        editable=False  
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Optional expiration datetime."
    )

    def save(self, *args, **kwargs):
        """
        Auto-generate a unique short code before saving if it's not already set.
        """
        if not self.code:
            self.code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self, length=6):
        """
        Generate a truly unique code by checking for duplicates in the DB.
        """
        while True:
            code = generate_unique_code(length)
            if not ShortenedURL.objects.filter(code=code).exists():
                return code

    def get_short_url(self):
        """
        Returns the complete shortened URL including the domain.
        """
        domain = getattr(settings, "BASE_DOMAIN", "http://localhost:8000")
        return f"{domain}/{self.code}"

    def is_expired(self):
        """
        Checks if the short URL has expired based on the current time.
        """
        return self.expires_at is not None and timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.get_short_url()} → {self.long_url}"
