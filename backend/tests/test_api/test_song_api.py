import pytest

import json
from http import HTTPStatus


@pytest.mark.django_db()
class TestSongAPI:
    def test_00_get_all_songs(
        self, api_client, artist_model, album_model, song_model
    ) -> None:
        endpoint = "/api/v1/songs/"
        artist = artist_model.objects.create(name="qurixsity")
        album = album_model.objects.create(
            name="Oops", artist=artist, year=2023
        )
        song_1 = song_model.objects.create(
            name="A_Exposition", album=album, serial_number_in_album=1
        )
        song_2 = song_model.objects.create(
            name="B_Disposition", album=album, serial_number_in_album=2
        )
        expected_data = [
            {
                "id": song_1.id,
                "name": song_1.name,
                "album": album.name,
                "serial_number_in_album": song_1.serial_number_in_album,
            },
            {
                "id": song_2.id,
                "name": song_2.name,
                "album": album.name,
                "serial_number_in_album": song_2.serial_number_in_album,
            },
        ]
        response = api_client.get(path=endpoint)
        assert (
            response.status_code == HTTPStatus.OK
        ), (
            f'При "GET" запросе на эндпоинт "{endpoint}" '
            f'должен возвращаться код {HTTPStatus.OK}.'
        )
        assert (
            json.loads(response.content).get("results") == expected_data
        ), (
            'Структура ответа API при "GET" запросе '
            f'на эндпоинт "{endpoint}" отличается от заявленной.'
        )

    def test_01_get_concrete_song(
        self, api_client, artist_model, album_model, song_model
    ):
        artist = artist_model.objects.create(name="StopBan")
        album = album_model.objects.create(
            name="Kiss", artist=artist, year=2023
        )
        song = song_model.objects.create(
            name="Course", album=album, serial_number_in_album=1
        )
        endpoint = f"/api/v1/songs/{song.id}/"
        expected_data = {
            "id": song.id,
            "name": song.name,
            "album": album.name,
            "serial_number_in_album": song.serial_number_in_album,
        }
        response = api_client.get(path=endpoint)
        assert (
            response.status_code == HTTPStatus.OK
        ), (
            f'При "GET" запросе на эндпоинт "{endpoint}" '
            f'должен возвращаться код {HTTPStatus.OK}.'
        )
        assert (
            json.loads(response.content) == expected_data
        ), (
            'Структура ответа API при "GET" запросе '
            f'на эндпоинт "{endpoint}" отличается от заявленной.'
        )

    def test_02_create_new_song(
        self, api_client, artist_model, album_model, song_model
    ) -> None:
        endpoint = "/api/v1/songs/"
        artist = artist_model.objects.create(name="Kingston")
        album = album_model.objects.create(
            name="Boston", artist=artist, year=2021
        )
        post_data = {"name": "Crystalys", "album": album.id}
        quantity_before_request = song_model.objects.count()
        expected_data = {
            "id": quantity_before_request + 1,
            "name": post_data.get("name"),
            "album": album.name,
            "serial_number_in_album": 1,
        }
        response = api_client.post(path=endpoint, data=post_data)
        quantity_after_request = song_model.objects.count()
        assert (
            response.status_code == HTTPStatus.CREATED
        ), (
            f'При "POST" запросе на эндпоинт "{endpoint}" '
            f'должен возвращаться код {HTTPStatus.CREATED}.'
        )
        assert expected_data == json.loads(
            response.content
        ), (
            'Структура ответа API при "POST" запросе '
            f'на эндпоинт "{endpoint}" отличается от заявленной.'
        )
        assert (
            quantity_before_request + 1 == quantity_after_request
        ), (
            f'При "POST" запросе на эндпоинт "{endpoint}" '
            'должна создаваться новая запись в базе данных.'
        )

    def test_03_partial_update_existing_song(
        self, api_client, artist_model, album_model, song_model
    ) -> None:
        artist = artist_model.objects.create(name="Kirya")
        album = album_model.objects.create(
            name="Two days ago", artist=artist, year=2013
        )
        song = song_model.objects.create(
            name="I'm bored", album=album, serial_number_in_album=1
        )
        endpoint = f"/api/v1/songs/{song.id}/"
        patch_data = {"name": "I'm not bored"}
        expected_data = {
            "id": song.id,
            "name": patch_data.get("name"),
            "album": album.name,
            "serial_number_in_album": song.serial_number_in_album,
        }
        response = api_client.patch(path=endpoint, data=patch_data)
        song = song_model.objects.get(id=song.id)
        assert (
            response.status_code == HTTPStatus.OK
        ), (
            f'При "PATCH" запросе на эндпоинт "{endpoint}" '
            f'должен возвращаться код {HTTPStatus.OK}.'
        )
        assert expected_data == json.loads(
            response.content
        ), (
            'Структура ответа API при "PATCH" запросе '
            f'на эндпоинт "{endpoint}" отличается от заявленной.'
        )
        assert song.name == patch_data.get(
            "name"
        ), (
            f'При "PATCH" запросе на эндпоинт "{endpoint}" '
            'объект модели базы данных должен изменяться.'
        )

    def test_04_complete_update_existing_song(
        self, api_client, artist_model, album_model, song_model
    ) -> None:
        artist = artist_model.objects.create(name="Roses")
        album = album_model.objects.create(
            name="Blackly", artist=artist, year=2014
        )
        song = song_model.objects.create(
            name="Highway", album=album, serial_number_in_album=1
        )
        endpoint = f"/api/v1/songs/{song.id}/"
        put_data = {"name": "NOT Highway", "album": album.id}
        expected_data = {
            "id": song.id,
            "name": put_data.get("name"),
            "album": album.name,
            "serial_number_in_album": song.serial_number_in_album,
        }
        response = api_client.put(path=endpoint, data={"name": "NOT Highway"})
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), (
            f'При "PUT" запросе на эндпоинт "{endpoint}" '
            'без обязательных полей '
            f'должен возвращаться код {HTTPStatus.BAD_REQUEST}.'
        )
        response = api_client.put(path=endpoint, data=put_data)
        song = song_model.objects.get(id=song.id)
        assert (
            response.status_code == HTTPStatus.OK
        ), (
            f'При "PUT" запросе на эндпоинт "{endpoint}" '
            f'должен возвращаться код {HTTPStatus.OK}.'
        )
        assert expected_data == json.loads(
            response.content
        ), (
            'Структура ответа API при "PUT" запросе '
            f'на эндпоинт "{endpoint}" отличается от заявленной.'
        )
        assert song.name == put_data.get(
            "name"
        ), (
            f'При "PUT" запросе на эндпоинт "{endpoint}" '
            'объект модели базы данных должен изменяться.'
        )

    def test_05_delete_existing_album(
        self, api_client, artist_model, album_model, song_model
    ) -> None:
        artist = artist_model.objects.create(name="mazeloff")
        album = album_model.objects.create(
            name="egoist", artist=artist, year=2023
        )
        song = song_model.objects.create(
            name="Marina", album=album, serial_number_in_album=1
        )
        endpoint = f"/api/v1/songs/{song.id}/"
        expected_data = b""
        quantity_before_request = song_model.objects.count()
        response = api_client.delete(path=endpoint)
        quantity_after_request = song_model.objects.count()
        assert (
            response.status_code == HTTPStatus.NO_CONTENT
        ), (
            f'При "DELETE" запросе на эндпоинт "{endpoint}" '
            f'должен возвращаться код {HTTPStatus.NO_CONTENT}.'
        )
        assert (
            expected_data == response.content
        ), (
            'Структура ответа API при "DELETE" запросе '
            f'на эндпоинт "{endpoint}" отличается от заявленной.'
        )
        assert (
            quantity_before_request - 1 == quantity_after_request
        ), (
            f'При "DELETE" запросе на эндпоинт "{endpoint}" '
            'должна удаляться запись из базы данных.'
        )

    def test_06_song_not_found(self, api_client):
        endpoint = "/api/v1/songs/1000/"
        response = api_client.get(path=endpoint)
        assert (
            response.status_code == HTTPStatus.NOT_FOUND
        ), (
            f'При запросе к конкретной песне, например "{endpoint}", '
            'в случае, если объект не существует - должен '
            f'возвращаться код {HTTPStatus.NOT_FOUND}.'
        )
