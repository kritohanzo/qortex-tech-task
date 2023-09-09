from django.db.models.signals import post_delete, post_save
from django.db.models import signals
from django.dispatch import receiver
from music.models import Song

@receiver(post_delete, sender=Song)
def rearrange_serial_numbers(sender: Song, instance: Song, *args, **kwargs) -> None:
    songs = instance.album.songs.order_by("serial_number_in_album")
    for i, song in enumerate(songs):
        song.serial_number_in_album = i + 1
        song.save()