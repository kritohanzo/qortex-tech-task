from rest_framework.routers import DefaultRouter
from api.v1.views import ArtistViewSet, AlbumViewSet, SongViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"artists", ArtistViewSet, basename="artists")
router.register(r"albums", AlbumViewSet, basename="albums")
router.register(r"songs", SongViewSet, basename="songs")

urlpatterns = [
    path('', include(router.urls)),
]
