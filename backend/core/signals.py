from django.db.models.signals import post_delete
from django.dispatch import receiver

from music.models import Song


@receiver(post_delete, sender=Song)
def rearrange_serial_numbers(
    sender: Song, instance: Song, *args, **kwargs
) -> None:
    """Сигнал для автоматического пересчёта
    порядкового номера песни в альбоме.

    После удаления песни получает queryset
    со всеми песнями, которые имеют больший порядковый номер,
    чем удалённая песня, после чего уменьшает их порядковый
    номер на 1.
    """
    songs = instance.album.songs.filter(
        serial_number_in_album__gt=instance.serial_number_in_album
    )
    for song in songs:
        song.serial_number_in_album -= 1
        song.save
