import pytest


@pytest.mark.django_db()
class TestMusicModels:
    def test_00_models_have_correct_str(
        self, artist_model, album_model, song_model
    ):
        artist = artist_model.objects.create(name="GHOSTMANE")
        album = album_model.objects.create(
            name="OPENWOODS", artist=artist, year=2022
        )
        song = song_model.objects.create(
            name="HUMAN TALKING", album=album, serial_number_in_album=1
        )
        object_expected = {
            artist: artist.name,
            album: album.name,
            song: song.name,
        }
        for object, expected in object_expected.items():
            assert str(object) == expected, (
                f"Объект модели {object.__class__.__name__} "
                "имеет некорректный __str__."
            )

    def test_01_models_have_correct_verbose_names(
        self, artist_model, album_model, song_model
    ):
        models_expected_fields = {
            artist_model: {"name": "Название"},
            album_model: {
                "name": "Название",
                "artist": "Исполнитель",
                "year": "Год выпуска",
            },
            song_model: {
                "name": "Название",
                "album": "Альбом",
                "serial_number_in_album": "Порядковый номер в альбоме",
            },
        }
        for model, expected_fields in models_expected_fields.items():
            for field, expected_verbose_name in expected_fields.items():
                assert (
                    model._meta.get_field(field).verbose_name
                    == expected_verbose_name
                )
