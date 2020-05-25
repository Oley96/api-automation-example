from faker import Faker


class User:

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def from_faker(cls):
        data = {
            "username": Faker().name(),
            "password": Faker().password(),
            "email": Faker().email()
        }
        return cls(**data)

    @property
    def get_user(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email
        }