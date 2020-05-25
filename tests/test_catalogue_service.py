from hamcrest import has_length, not_
from hamcrest.library.collection import is_empty
import pytest
from src.conditions import status_code, body, content_type, field_with_value, fields, validation_with_json_schema
from src.services import CatalogueApiService


@pytest.mark.api
@pytest.mark.positive
def test_get_list_of_products():
    CatalogueApiService().get_all_products() \
        .should_have(status_code(200)) \
        .should_have(content_type("text/plain")) \
        .should_have(body("$..id", has_length(9))) \
        .should_have(body("$.[0].name", "Holy"))


@pytest.mark.api
@pytest.mark.positive
def test_get_product():
    product = CatalogueApiService().get_featured_product(1)

    CatalogueApiService().get_product(product["id"]) \
        .should_have(status_code(200)) \
        .should_have(content_type("text/plain")) \
        .should_have(field_with_value("id", product["id"])) \
        .should_have(field_with_value("name", product["name"])) \
        .should_have(field_with_value("description", product["description"])) \
        .should_have(field_with_value("price", product["price"])) \
        .should_have(fields("tag", "count")) \
        .should_have(validation_with_json_schema("/schemas/product_schema.json"))


@pytest.mark.api
@pytest.mark.positive
def test_get_products_count():
    size = CatalogueApiService().count_all_products()

    CatalogueApiService().get_products_count() \
        .should_have(status_code(200)) \
        .should_have(content_type("text/plain")) \
        .should_have(field_with_value("size", size)) \
        .should_have(body("$.err", None))


@pytest.mark.api
@pytest.mark.positive
def test_get_products_tags():
    CatalogueApiService().get_tags() \
        .should_have(status_code(200)) \
        .should_have(content_type("text/plain")) \
        .should_have(body("$.tags", not_(is_empty))) \
        .should_have(body("$.tags[*]", has_length(11)))
