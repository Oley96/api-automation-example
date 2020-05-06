import pytest
from src.models.user import User


@pytest.fixture
def fake_user():
    return User.from_faker().get_user()
