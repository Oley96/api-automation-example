from hamcrest import has_length, greater_than
import pytest
from src.conditions import status_code, body, content_type, only_fields, validation_with_json_schema
from src.services import UserApiService


@pytest.mark.api
@pytest.mark.positive
def test_can_register_user_with_valid_credentials(fake_user):
    UserApiService().register_customer(fake_user) \
        .should_have(status_code(200)) \
        .should_have(only_fields("id"))


@pytest.mark.api
@pytest.mark.negative
def test_can_not_register_user_with_valid_credentials_twice(fake_user):
    UserApiService().register_customer(fake_user) \
        .should_have(status_code(200)) \
        .should_have(only_fields("id"))

    UserApiService().register_customer(fake_user) \
        .should_have(status_code(500))


@pytest.mark.api
@pytest.mark.positive
def test_user_should_login_with_valid_credentials(fake_user):
    UserApiService().register_customer(fake_user)
    UserApiService().login_with(fake_user) \
        .should_have(status_code(200)) \
        .should_have(content_type("text/html"))


@pytest.mark.api
@pytest.mark.negative
def test_user_should_not_login_without_credentials():
    UserApiService().login() \
        .should_have(content_type("text/plain")) \
        .should_have(status_code(401))


@pytest.mark.api
@pytest.mark.positive
def test_get_customers():
    UserApiService().get_customers() \
        .should_have(status_code(200)) \
        .should_have(content_type("text/plain")) \
        .should_have(body("$._embedded.customer[*]", has_length(greater_than(5)))) \
        .should_have(body("$..id", has_length(greater_than(5)))) \
        .should_have(body("$._embedded.customer[0].username", "Sandy Young"))


@pytest.mark.api
@pytest.mark.positive
def test_get_specific_customer(fake_user):
    id = UserApiService().register_customer(fake_user).json("id")

    UserApiService().get_customer(id) \
        .should_have(status_code(200)) \
        .should_have(content_type("text/plain"))


@pytest.mark.api
@pytest.mark.positive
def test_delete_customer_by_id(fake_user):
    id = UserApiService().register_customer(fake_user).json("id")

    UserApiService().delete_customer(id) \
        .should_have(status_code(200)) \
        .should_have(content_type("text/plain")) \
        .should_have(body("$.status", True))


@pytest.mark.api
@pytest.mark.positive
def test_get_addresses():
    UserApiService().get_addresses() \
        .should_have(status_code(200)) \
        .should_have(content_type("text/plain")) \
        .should_have(only_fields("_embedded")) \
        .should_have(body("$._embedded.address[0].street", "my road")) \
        .should_have(body("$._embedded.address[0].country", "UK")) \
        .should_have(body("$._embedded.address[0].city", "London")) \
        .should_have(validation_with_json_schema("/schemas/address_schema.json"))
