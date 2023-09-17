import pytest

import json
from http import HTTPStatus


@pytest.mark.django_db()
class TestArtistAPI:
    def test_00_get_all_artists(self, api_client, artist_model) -> None:
        endpoint = "/api/v1/artists/"
        artist_1 = artist_model.objects.create(name="A_Max")
        artist_2 = artist_model.objects.create(name="B_Korzh")
        expected_data = [
            {"id": artist_1.id, "name": artist_1.name},
            {"id": artist_2.id, "name": artist_2.name},
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

    def test_01_get_concrete_artist(self, api_client, artist_model):
        artist = artist_model.objects.create(name="Toxi$")
        endpoint = f"/api/v1/artists/{artist.id}/"
        expected_data = {"id": artist.id, "name": artist.name}
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

    def test_02_create_new_artist(self, api_client, artist_model) -> None:
        endpoint = "/api/v1/artists/"
        post_data = {"name": "pyatno"}
        quantity_before_request = artist_model.objects.count()
        expected_data = {
            "id": quantity_before_request + 1,
            "name": post_data.get("name")
        }
        response = api_client.post(path=endpoint, data=post_data)
        quantity_after_request = artist_model.objects.count()
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

    def test_03_partial_update_existing_artist(
        self, api_client, artist_model
    ) -> None:
        artist = artist_model.objects.create(name="ROONIN")
        endpoint = f"/api/v1/artists/{artist.id}/"
        patch_data = {"name": "NOT ROONIN"}
        expected_data = {"id": artist.id, "name": patch_data.get("name")}
        response = api_client.patch(path=endpoint, data=patch_data)
        artist = artist_model.objects.get(id=artist.id)
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
        assert artist.name == patch_data.get(
            "name"
        ), (
            f'При "PATCH" запросе на эндпоинт "{endpoint}" объект '
            'модели базы данных должен изменяться.'
        )

    def test_04_complete_update_existing_artist(
        self, api_client, artist_model
    ) -> None:
        artist = artist_model.objects.create(name="STRLGHT")
        endpoint = f"/api/v1/artists/{artist.id}/"
        put_data = {"name": "NOT STRLGHT"}
        expected_data = {"id": artist.id, "name": put_data.get("name")}
        response = api_client.put(path=endpoint, data={})
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), (
            f'При "PUT" запросе на эндпоинт "{endpoint}" без обязательных '
            f'полей должен возвращаться код {HTTPStatus.BAD_REQUEST}.'
        )
        response = api_client.put(path=endpoint, data=put_data)
        artist = artist_model.objects.get(id=artist.id)
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
        assert artist.name == put_data.get(
            "name"
        ), (
            f'При "PUT" запросе на эндпоинт "{endpoint}" объект '
            'модели базы данных должен изменяться.'
        )

    def test_05_delete_existing_artist(self, api_client, artist_model) -> None:
        artist = artist_model.objects.create(name="STED.D")
        endpoint = f"/api/v1/artists/{artist.id}/"
        expected_data = b""
        quantity_before_request = artist_model.objects.count()
        response = api_client.delete(path=endpoint)
        quantity_after_request = artist_model.objects.count()
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

    def test_06_artist_not_found(self, api_client):
        endpoint = "/api/v1/artists/1000/"
        response = api_client.get(path=endpoint)
        assert (
            response.status_code == HTTPStatus.NOT_FOUND
        ), (
            f'При запросе к конкретному исполнителю, например "{endpoint}", '
            'в случае, если объект не существует - должен '
            f'возвращаться код {HTTPStatus.NOT_FOUND}.'
        )
