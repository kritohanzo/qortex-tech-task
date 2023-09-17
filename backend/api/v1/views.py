from typing import Optional, Type

from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import (ArtistSerializer, CreateUpdateAlbumSerializer,
                                CreateUpdateSongSerializer,
                                RetrieveListAlbumSerializer,
                                RetrieveListSongSerializer,)
from music.models import Album, Artist, Song


class MultiSerializerViewSetMixin:
    """Миксин для выбора нужного сериализатора из `serializer_classes`."""

    serializer_classes: Optional[dict[str, Type[Serializer]]] = None

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return super().get_serializer_class()


class ArtistViewSet(ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()


class AlbumViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    queryset = Album.objects.select_related("artist")

    serializer_classes = {
        "create": CreateUpdateAlbumSerializer,
        "update": CreateUpdateAlbumSerializer,
        "partial_update": CreateUpdateAlbumSerializer,
        "list": RetrieveListAlbumSerializer,
        "retrieve": RetrieveListAlbumSerializer,
    }


class SongViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    queryset = Song.objects.select_related("album")

    serializer_classes = {
        "create": CreateUpdateSongSerializer,
        "update": CreateUpdateSongSerializer,
        "partial_update": CreateUpdateSongSerializer,
        "list": RetrieveListSongSerializer,
        "retrieve": RetrieveListSongSerializer,
    }

    def perform_create(self, serializer):
        album = serializer.validated_data.get("album")
        songs = album.songs.all()
        serial_number_in_album = len(songs) + 1
        serializer.save(serial_number_in_album=serial_number_in_album)
