from datetime import datetime

from django.core.exceptions import ValidationError


def validate_album_year(year: int) -> int:
    """Функция-валидатор, проверяющая,
    что пользователь ввёл корректный год.

    Args:
        year (int):
            Год, введённый пользователем.

    Raises:
        ValidationError:
            Год, введённый пользователем меньше 1 или больше текущего.
    """
    now = datetime.now()
    if not 0 < year <= now.year:
        raise ValidationError(
            "Год должен быть больше 0 и не меньше текущего года!"
        )
    return year
