from http import HTTPStatus

def create_artist(url, client, artist_name):
    data = {"name": artist_name}
    response = client.post(url=url, data=data)
    assert response.status_code == HTTPStatus.CREATED, (
        'Если POST-запрос авторизованного пользователя к '
        '`/api/v1/titles/{title_id}/reviews/{review_id}/comments/` содержит '
        'корректные данные - должен вернуться ответ со статусом 201.'
    )
    return response