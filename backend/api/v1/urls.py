from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.v1.views import AlbumViewSet, ArtistViewSet, SongViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Music API",
      default_version='v1',
      description="123",
      contact=openapi.Contact(url="https://t.me/kritohanzo"),
   ),
   public=True,
)

router = DefaultRouter()
router.register(r"artists", ArtistViewSet, basename="artists")
router.register(r"albums", AlbumViewSet, basename="albums")
router.register(r"songs", SongViewSet, basename="songs")

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("", include(router.urls)),
]
