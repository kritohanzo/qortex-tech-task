# Тестовое задание компании Qortex / API музыкального хранилища

### Что было сделано?
* В качестве базы данных выбрана PostgreSQL;
* Написаны модели, вьюсеты и сериализаторы для исполнителей, альбомов и песен;
* Версионированное API, которое в дальнешем легко расширять;
* Команда для manage.py: import_json позволяет импортировать данные в модели из JSON файлов.
* С помощью метода вьюсета permorm_create и сигналов Django добавлены автовыдача порядкого номера песни в альбоме и перерасчёт номеров, в случае удаления песни из середины альбома;
* Подключён Swagger: документация доступна по эндпоинту '/api/v1/docs/';
* Написаны тесты для моделей и API, используя Pytest;
* Настроен Github Workflows, при пуше в ветку 'dev' запускаются тесты, проверяющие код на соответствие PEP8 и работоспособность.
* Проект разворачивается в 3-ёх контейнерах: DB, backend, nginx;

## Как запустить проект локально?

### Ручной запуск:
* Клонируйте репозиторий к себе на ПК:
```
git clone https://github.com/kritohanzo/qortex-tech-task.git
```
* Перейдите в директорию, отвечающую за backend:
```
cd qortex-tech-task/backend
```
* Создайте новое виртуальное окружение и работайте через него:
```
python -m venv venv
source venv/Scripts/activate (для windows)
source venv/bin/activate (для linux)
```
* Установите зависимости, необходимые для запуска backend части проекта:
```
pip install -r requirements/requirements.project.txt
```
* Разверните сервер PostgreSQL, либо поменяйте базу данных в настройках проекта, как показано ниже:
```
# main/settings.py
# замените имеющуюся константу DATABASES, на ту, которая показана ниже

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```
* В случае, если вы развернули сервер PostgreSQL - создайте файл '.env' и укажите информацию о вашем сервере, как в примере ниже:
```
POSTGRES_USER="django_user"
POSTGRES_PASSWORD="django_password"
POSTGRES_DB="django"
DB_HOST="127.0.0.1"
DB_PORT="5432"
```
* Выполните миграции и запустите проект:
```
python manage.py migrate
python manage.py runserver
```
* Если вам нужны тестовые данные, выполните 3 команды:
```
python manage.py import_json -f data/artists.json -a music -m Artist
python manage.py import_json -f data/albums.json -a music -m Album
python manage.py import_json -f data/songs.json -a music -m Song
```
* Откройте браузер и зайдите на '*127.0.0.1:8000/api/v1/*', у вас загрузится страница проекта.
* Для просмотра тестовых запросов, по желанию, вы можете использовать файл requests.http, который лежит в папке проекта (требует расширения REST Client для VSCode).

### Автоматический запуск (Docker):
* Клонируйте репозиторий к себе на ПК:
```
git clone https://github.com/kritohanzo/qortex-tech-task.git
```
* Перейдите в директорию репозитория:
```
cd qortex-tech-task
```
* Запустите docker-compose, который соберёт образы на основе Dockerfile, которые лежат в папках 'backend' и 'nginx':
```
sudo docker compose -f docker-compose.yml up
```
* Откройте браузер и зайдите на '*localhost*', у вас загрузится страница проекта.
