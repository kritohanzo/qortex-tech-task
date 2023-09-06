from django.contrib import admin
from music.models import Artist, Album, Song

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

@admin.register(Song)
class SongConfig(admin.ModelAdmin):
    list_display = ["id", "name", "album", "serial_number_in_album"]
    list_display_links = ["id", "name"]
    search_fields = ["name", "album"]
    empty_value_display = EMPTY_VALUE_DISPLAY