from django.db import models

from core.validators import validate_album_year


class Artist(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название")

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название")
    artist = models.ForeignKey(
        to=Artist,
        on_delete=models.CASCADE,
        related_name="albums",
        verbose_name="Исполнитель",
    )
    year = models.PositiveSmallIntegerField(
        validators=[validate_album_year], verbose_name="Год выпуска"
    )

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=128, verbose_name="Название")
    album = models.ForeignKey(
        to=Album,
        on_delete=models.CASCADE,
        related_name="songs",
        verbose_name="Альбом",
    )
    serial_number_in_album = models.PositiveIntegerField(
        verbose_name="Порядковый номер в альбоме"
    )

    class Meta:
        verbose_name = "Песня"
        verbose_name_plural = "Песни"
        ordering = ("name",)

    def __str__(self):
        return self.name
