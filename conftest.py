import pytest

from src.models.card import Card
from src.models.user import User


@pytest.fixture
def fake_user():
    return User.from_faker().get_user()


@pytest.fixture
def fake_card():
    def _get_card(user_id):
        return Card.from_faker(user_id).card

    return _get_card