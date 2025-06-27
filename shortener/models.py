from django.conf import settings
from django.db import models
from django.utils import timezone

from .random import generate_unique_code


class ShortenedURL(models.Model):
    """
    Model to store original long URLs and their corresponding auto-generated short codes.
    Includes creation timestamp and optional expiration.
    """

    long_url = models.URLField(help_text="Original long URL")
    code = models.CharField(max_length=10, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overridden save method to:
        - Auto-generate a unique short code if not provided.
        - Auto-set an expiration time (7 days from now) if not provided.
        """
        if not self.code:
            self.code = self._generate_unique_code()

        # Set default expiration to 7 days from now if not already set
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)

        super().save(*args, **kwargs)

    def _generate_unique_code(self, length=6):
        """
        Helper method to generate a unique short code of given length.
        Ensures no duplicate code exists in the database.
        """
        while True:
            code = generate_unique_code(length)
            if not ShortenedURL.objects.filter(code=code).exists():
                return code

    def is_expired(self):
        """
        Returns True if the URL has expired based on `expires_at`.
        If `expires_at` is None, it's considered not expired.
        """
        return self.expires_at and timezone.now() > self.expires_at

    def __str__(self):
        """
        String representation of the ShortenedURL object.

        """
        return f"{self.code} → {self.long_url}"
