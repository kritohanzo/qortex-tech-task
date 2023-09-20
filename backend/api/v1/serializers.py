from rest_framework import serializers

from music.models import Album, Artist, Song


class ArtistSerializer(serializers.ModelSerializer):
    """Серилизатор для модели исполнителя."""

    class Meta:
        model = Artist
        fields = ("id", "name")


class CreateUpdateAlbumSerializer(serializers.ModelSerializer):
    """Серилизатор для модели альбома.

    Отрабатывает исключительно при создании новых
    или обновлении существующих записей альбомов в БД.
    """

    class Meta:
        model = Album
        fields = ("id", "name", "artist", "year")

    def to_representation(self, instance):
        """Переопеделние метода,
        срабатывающего при возврате ответа от API.

        При возврате ответа от API использует сериализатор,
        предназначенный для более подробного вывода информации,
        заменяющий ID объектов на их имена.
        """
        request = self.context.get("request")
        return RetrieveListAlbumSerializer(
            instance=instance, context={"request": request}
        ).data


class CreateUpdateSongSerializer(serializers.ModelSerializer):
    """Серилизатор для модели песни.

    Отрабатывает исключительно при создании новых
    или обновлении существующих записей песен в БД.
    """

    class Meta:
        model = Song
        fields = ("id", "name", "album", "serial_number_in_album")
        read_only_fields = ("serial_number_in_album",)

    def to_representation(self, instance):
        """Переопеделние метода,
        срабатывающего при возврате ответа от API.

        При возврате ответа от API использует сериализатор,
        предназначенный для более подробного вывода информации,
        заменяющий ID объектов на их имена.
        """
        request = self.context.get("request")
        return RetrieveListSongSerializer(
            instance=instance, context={"request": request}
        ).data


class RetrieveListAlbumSerializer(serializers.ModelSerializer):
    """Серилизатор для модели альбома.

    Отрабатывает для любом выводе информации об альбомах,
    поскольку вместо ID объектов содержит их имена.
    """

    artist = serializers.CharField(source="artist.name")

    class Meta:
        model = Album
        fields = ("id", "name", "artist", "year")


class RetrieveListSongSerializer(serializers.ModelSerializer):
    """Серилизатор для модели песни.

    Отрабатывает для любом выводе информации об песнях,
    поскольку вместо ID объектов содержит их имена.
    """

    album = serializers.CharField(source="album.name")

    class Meta:
        model = Song
        fields = ("id", "name", "album", "serial_number_in_album")
