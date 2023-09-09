from http import HTTPStatus

import pytest
from tests.utils import create_artist

@pytest.mark.django_db(transaction=True)
class Test00ArtistsAPI:

    def test_01_endpoint_exists(self, client):
        response = client.get("http://127.0.0.1:8000/api/v1/artists/")
        assert response.status_code == HTTPStatus.OK