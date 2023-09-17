import pytest

from rest_framework.test import APIClient
from django.apps import apps
from django.db.models import Model
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "127.0.0.1",
        "NAME": "test_db",
        "PASSWORD": "test_password",
        "USER": "test_user",
        "PORT": 5432,
    }


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
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
