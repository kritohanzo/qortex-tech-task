from django.db.models.signals import post_delete, post_save
from django.db.models import signals
from django.dispatch import receiver
from music.models import Song

@receiver(post_delete, sender=Song)
def rearrange_serial_numbers(sender: Song, instance: Song, *args, **kwargs) -> None:
    print("zdarova")
    songs = instance.album.songs.all()
    print(songs)
    for i, song in enumerate(songs):
        song.id = i + 1
        song.save()