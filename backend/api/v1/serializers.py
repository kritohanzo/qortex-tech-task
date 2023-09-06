from rest_framework import serializers
from music.models import Artist, Album, Song

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "name")

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("id", "artist", "year")

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("id", "name", "album", "serial_number_in_album")
        read_only_fields = ("serial_number_in_album",)