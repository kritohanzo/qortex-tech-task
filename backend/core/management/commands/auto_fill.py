import json
import os
from pathlib import Path

from progress.bar import PixelBar

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = Path(__file__).parent.parent.parent.parent / "data"
        app_names = os.listdir(path)
        for app_name in app_names:
            app_path = os.path.join(path, app_name)
            data_names = os.listdir(app_path)
            for data_name in data_names:
                data_path = os.path.join(app_path, data_name)
                django_model = apps.get_model(
                    app_label=app_name, model_name=data_name[:-6]
                )
                with open(data_path, "r", encoding="utf-8") as file:
                    try:
                        text = json.load(file)
                    except TypeError:
                        try:
                            text = json.loads(file.readlines()[0])
                        except TypeError:
                            raise CommandError("Получен невалидный JSON!")
                    bar = PixelBar(
                        f"Добавление данных в модель {django_model.__name__}",
                        max=len(text),
                    )
                    for item in text:
                        django_model.objects.create(**item)
                        bar.next()
                bar.finish()
