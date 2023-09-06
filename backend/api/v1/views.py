from rest_framework.viewsets import ModelViewSet
from api.v1.serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from music.models import Artist, Album, Song

class ArtistViewSet(ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()

class AlbumViewSet(ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.select_related("artist")

class SongViewSet(ModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.select_related("album")

    def perform_create(self, serializer):
        serial_number_in_album = len(self.queryset) + 1
        serializer.save(serial_number_in_album=serial_number_in_album)