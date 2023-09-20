from typing import Optional, Type

from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import (ArtistSerializer, CreateUpdateAlbumSerializer,
                                CreateUpdateSongSerializer,
                                RetrieveListAlbumSerializer,
                                RetrieveListSongSerializer,)
from music.models import Album, Artist, Song


class MultiSerializerViewSetMixin:
    """Миксин для выбора нужного сериализатора из "serializer_classes".

    Позволяет задать словарь в классе вьюсета,
    после чего миксин будет самостоятельно выбирать
    нужный сериализатор, в зависимости от action.

    Например:
        serializer_classes = {
            ...,
            "retrieve": RetrieveUserSerializer,
            ...
        }
    """

    serializer_classes: Optional[dict[str, Type[Serializer]]] = None

    def get_serializer_class(self):
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return super().get_serializer_class()


class ArtistViewSet(ModelViewSet):
    """Вьюсет для модели исполнителя."""

    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()


class AlbumViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """Вьюсет для модели альбома."""

    queryset = Album.objects.select_related("artist")
    serializer_classes = {
        "create": CreateUpdateAlbumSerializer,
        "update": CreateUpdateAlbumSerializer,
        "partial_update": CreateUpdateAlbumSerializer,
        "list": RetrieveListAlbumSerializer,
        "retrieve": RetrieveListAlbumSerializer,
    }


class SongViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """Вьюсет для модели песни."""

    queryset = Song.objects.select_related("album")
    serializer_classes = {
        "create": CreateUpdateSongSerializer,
        "update": CreateUpdateSongSerializer,
        "partial_update": CreateUpdateSongSerializer,
        "list": RetrieveListSongSerializer,
        "retrieve": RetrieveListSongSerializer,
    }

    def perform_create(self, serializer):
        """Переопеделние метода,
        срабатывающего перед созданием новой песни в БД.

        Перед созданием песни присвает ей порядковый номер в альбоме,
        равный количеству всех имеющихся песен в конкретном альбоме плюс один.
        """
        album = serializer.validated_data.get("album")
        songs = album.songs.all()
        serial_number_in_album = len(songs) + 1
        serializer.save(serial_number_in_album=serial_number_in_album)
