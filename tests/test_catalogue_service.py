from hamcrest import has_length, greater_than, not_
from hamcrest.library.collection import is_empty

from src.conditions import status_code, body
from src.services import CatalogueApiService


def test_get_catalogue():
    CatalogueApiService().get_all_products() \
        .should_have(status_code(200)) \
        .should_have(body("$..id", has_length(greater_than(0))))


def test_get_item_by_id():
    id = CatalogueApiService().get_featured_item_id(1)

    CatalogueApiService().get_item_by_id(id) \
        .should_have(status_code(200)) \
        .should_have(body("$.id", id))


def test_catalogue_size():
    size = CatalogueApiService().count_all_items()

    CatalogueApiService().get_products_count() \
        .should_have(status_code(200)) \
        .should_have(body("$.size", size))


def test_catalogue_tags():
    CatalogueApiService().get_tags() \
        .should_have(status_code(200)) \
        .should_have(body("$.tags", not_(is_empty)))
