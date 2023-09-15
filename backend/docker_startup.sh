#!/bin/sh
sleep 10
python manage.py migrate
python manage.py import_json -f data/artists.json -a music -m Artist
python manage.py import_json -f data/albums.json -a music -m Album
python manage.py import_json -f data/songs.json -a music -m Song
python manage.py collectstatic
cp -r /app/collected_static/. /backend_static/static/
gunicorn --bind 0.0.0.0:8000 backend.wsgi