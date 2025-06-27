from django.urls import path

from .views import ListShortenedURLsAPIView, RedirectURLAPIView, ShortenURLAPIView

urlpatterns = [
    path("api/shorten/", ShortenURLAPIView.as_view(), name="shorten-url"),
    path(
        "shortened-urls/",
        ListShortenedURLsAPIView.as_view(),
        name="list-shortened-urls",
    ),
    path("<str:code>/", RedirectURLAPIView.as_view(), name="redirect-url"),
]
