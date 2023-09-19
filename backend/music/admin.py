from django.contrib import admin

from music.models import Album, Artist, Song
from core.filters import ArtistFilter, AlbumFilter

admin.site.site_header = "Администрирование Qortex"
EMPTY_VALUE_DISPLAY = "—"


@admin.register(Artist)
class ArtistConfig(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Album)
class AlbumConfig(admin.ModelAdmin):
    list_display = ["id", "name", "artist", "year"]
    list_display_links = ["id", "name"]
    search_fields = ["artist", "year"]
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_filter = [ArtistFilter]

    def get_queryset(self, request):
        queryset = super(AlbumConfig, self).get_queryset(request).select_related("artist")
        return queryset 


@admin.register(Song)
class SongConfig(admin.ModelAdmin):
    list_display = ["id", "name", "album", "serial_number_in_album"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "album"]
    empty_value_display = EMPTY_VALUE_DISPLAY
    list_filter = [AlbumFilter]

    def get_queryset(self, request):
        queryset = super(SongConfig, self).get_queryset(request).select_related("album")
        return queryset 
