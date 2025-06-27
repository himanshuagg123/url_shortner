from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortenedURL
from .serializers import ShortenedURLSerializer


class ShortenURLAPIView(APIView):
    """
    POST /api/shorten/
    Accepts a long URL and (optionally) an expiry date, and returns a shortened URL.
    """

    def post(self, request):
        serializer = ShortenedURLSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()  # Save and auto-generate code/expiry if needed
            return Response(
                ShortenedURLSerializer(instance).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectURLAPIView(APIView):
    """
    GET /<code>/
    Looks up the short code and redirects to the original long URL if not expired.
    """

    def get(self, request, code):
        # Fetch object or return 404 if code not found
        url = get_object_or_404(ShortenedURL, code=code)

        # Check if the URL has expired
        if url.is_expired():
            raise NotFound(detail="This link has expired.")

        # Perform an actual HTTP 302 redirect to the long URL
        return redirect(url.long_url)


class ListShortenedURLsAPIView(APIView):
    """
    GET /api/shortened-urls/
    Returns a list of all shortened URLs stored in the system.
    Useful for debugging or admin purposes.
    """

    def get(self, request):
        urls = ShortenedURL.objects.all()
        serializer = ShortenedURLSerializer(urls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
