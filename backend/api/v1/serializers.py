from rest_framework import serializers
from music.models import Artist, Album, Song

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "name")

class CreateUpdateAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("id", "name", "artist", "year")

class CreateUpdateSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("id", "name", "album", "serial_number_in_album")
        read_only_fields = ("serial_number_in_album",)

class RetrieveListAlbumSerializer(serializers.ModelSerializer):
    artist = serializers.CharField(source="artist.name")
    class Meta:
        model = Album
        fields = ("id", "name", "artist", "year")

class RetrieveListSongSerializer(serializers.ModelSerializer):
    album = serializers.CharField(source="album.name")
    class Meta:
        model = Song
        fields = ("id", "name", "album", "serial_number_in_album")