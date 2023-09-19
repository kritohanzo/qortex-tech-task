from admin_auto_filters.filters import AutocompleteFilter


class ArtistFilter(AutocompleteFilter):
    """
    Фильтр для админки,
    позволяющий искать записи на основе поля 'artist'.
    """

    title = "Исполнитель"
    field_name = "artist"


class AlbumFilter(AutocompleteFilter):
    """
    Фильтр для админки,
    позволяющий искать записи на основе поля 'album'.
    """

    title = "Альбом"
    field_name = "album"