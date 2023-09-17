import pytest

from rest_framework.test import APIClient
from django.apps import apps
from django.db.models import Model


@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def artist_model() -> Model:
    return apps.get_model(app_label="music", model_name="Artist")


@pytest.fixture
def album_model() -> Model:
    return apps.get_model(app_label="music", model_name="Album")


@pytest.fixture
def song_model() -> Model:
    return apps.get_model(app_label="music", model_name="Song")
