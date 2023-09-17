import pytest

import json
from http import HTTPStatus


@pytest.mark.django_db()
class TestAlbumAPI:
    def test_00_get_all_albums(
        self, api_client, artist_model, album_model
    ) -> None:
        endpoint = "/api/v1/albums/"
        artist = artist_model.objects.create(name="HighSwag")
        album_1 = album_model.objects.create(
            name="A_Lyrics", artist=artist, year=2022
        )
        album_2 = album_model.objects.create(
            name="B_Lyrics", artist=artist, year=2023
        )
        expected_data = [
            {
                "id": album_1.id,
                "name": album_1.name,
                "artist": artist.name,
                "year": album_1.year,
            },
            {
                "id": album_2.id,
                "name": album_2.name,
                "artist": artist.name,
                "year": album_2.year,
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

    def test_01_get_concrete_album(
        self, api_client, artist_model, album_model
    ):
        artist = artist_model.objects.create(name="КУОК")
        album = album_model.objects.create(
            name="Sad history", artist=artist, year=2001
        )
        endpoint = f"/api/v1/albums/{album.id}/"
        expected_data = {
            "id": album.id,
            "name": album.name,
            "artist": artist.name,
            "year": album.year,
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

    def test_02_create_new_album(
        self, api_client, artist_model, album_model
    ) -> None:
        endpoint = "/api/v1/albums/"
        artist = artist_model.objects.create(name="Daylor")
        post_data = {"name": "miSShooting", "artist": artist.id, "year": 2008}
        quantity_before_request = album_model.objects.count()
        expected_data = {
            "id": quantity_before_request + 1,
            "name": post_data.get("name"),
            "artist": artist.name,
            "year": post_data.get("year"),
        }
        response = api_client.post(path=endpoint, data=post_data)
        quantity_after_request = album_model.objects.count()
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

    def test_03_partial_update_existing_album(
        self, api_client, artist_model, album_model
    ) -> None:
        artist = artist_model.objects.create(name="Mag Luzi")
        album = album_model.objects.create(
            name="Story of days", artist=artist, year=1987
        )
        endpoint = f"/api/v1/albums/{album.id}/"
        patch_data = {"name": "NOT Story of days"}
        expected_data = {
            "id": album.id,
            "name": patch_data.get("name"),
            "artist": artist.name,
            "year": album.year,
        }
        response = api_client.patch(path=endpoint, data=patch_data)
        album = album_model.objects.get(id=album.id)
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
        assert album.name == patch_data.get(
            "name"
        ), (
            f'При "PATCH" запросе на эндпоинт "{endpoint}" '
            'объект модели базы данных должен изменяться.'
        )

    def test_04_complete_update_existing_album(
        self, api_client, artist_model, album_model
    ) -> None:
        artist = artist_model.objects.create(name="rizza")
        album = album_model.objects.create(
            name="STOP THIS", artist=artist, year=2014
        )
        endpoint = f"/api/v1/albums/{album.id}/"
        put_data = {"name": "NOT STOP THIS", "artist": artist.id, "year": 2020}
        expected_data = {
            "id": album.id,
            "name": put_data.get("name"),
            "artist": artist.name,
            "year": put_data.get("year"),
        }
        response = api_client.put(
            path=endpoint, data={"name": "NOT STOP THIS"}
        )
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), (
            f'При "PUT" запросе на эндпоинт "{endpoint}" '
            'без обязательных полей '
            f'должен возвращаться код {HTTPStatus.BAD_REQUEST}.'
        )
        response = api_client.put(path=endpoint, data=put_data)
        album = album_model.objects.get(id=album.id)
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
        assert album.name == put_data.get(
            "name"
        ), (
            f'При "PUT" запросе на эндпоинт "{endpoint}" '
            'объект модели базы данных должен изменяться.'
        )

    def test_05_delete_existing_album(
        self, api_client, artist_model, album_model
    ) -> None:
        artist = artist_model.objects.create(name="katanacss")
        album = album_model.objects.create(
            name="KATANA", artist=artist, year=2023
        )
        endpoint = f"/api/v1/albums/{album.id}/"
        expected_data = b""
        quantity_before_request = album_model.objects.count()
        response = api_client.delete(path=endpoint)
        quantity_after_request = album_model.objects.count()
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

    def test_06_album_not_found(self, api_client):
        endpoint = "/api/v1/albums/1000/"
        response = api_client.get(path=endpoint)
        assert (
            response.status_code == HTTPStatus.NOT_FOUND
        ), (
            f'При запросе к конкретному альбому, например "{endpoint}", '
            'в случае, если объект не существует - должен '
            f'возвращаться код {HTTPStatus.NOT_FOUND}.'
        )
