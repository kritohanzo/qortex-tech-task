from django.db.models.signals import post_delete
from django.dispatch import receiver
from music.models import Song

@receiver(post_delete, sender=Song)
def rearrange_serial_numbers(sender: Song, instance: Song, *args, **kwargs) -> None:
    songs = instance.album.songs.filter(serial_number_in_album__gt=instance.serial_number_in_album)
    for song in songs:
        song.serial_number_in_album -= 1
        song.save