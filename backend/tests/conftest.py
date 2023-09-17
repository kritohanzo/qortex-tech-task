import pytest

from rest_framework.test import APIClient
from django.apps import apps
from django.db.models import Model

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


# @pytest.fixture(scope='session')
# def django_db_setup():
#     from django.conf import settings
#     settings.DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db_name.sqlite3',
#     }


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
