from hamcrest import has_length, greater_than

from src.conditions import status_code, body
from src.models import get_user
from src.services import UserApiService


def test_can_register_user_with_valid_credentials(faker):
    user = get_user(faker)

    UserApiService().register_customer(user) \
        .should_have(status_code(200)) \
        .should_have(body("$.id", has_length(greater_than(0))))


def test_can_not_register_user_with_valid_credentials_twice(faker):
    user = get_user(faker)

    UserApiService().register_customer(user) \
        .should_have(status_code(200)) \
        .should_have(body("$.id", has_length(greater_than(0))))

    UserApiService().register_customer(user) \
        .should_have(status_code(500))


def test_delete_customer_by_id(faker):
    user = get_user(faker)

    id = UserApiService().get_id(user)
    UserApiService().delete_customer(id) \
        .should_have(status_code(200)) \
        .should_have(body("$.status", True))


def test_get_customers():
    UserApiService().get_customers() \
        .should_have(status_code(200)) \
        .should_have(body("$._embedded.customer[*]", has_length(greater_than(5)))) \
        .should_have(body("$..id", has_length(greater_than(5)))) \
        .should_have(body("$._embedded.customer[0].username", "Sandy Young"))


def test_get_addresses():
    UserApiService().get_addresses() \
        .should_have(status_code(200)) \
        .should_have(body("$._embedded.address[0].street", "my road")) \
        .should_have(body("$._embedded.address[0].country", "UK")) \
        .should_have(body("$._embedded.address[0].city", "London"))

