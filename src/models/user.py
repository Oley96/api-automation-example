
class User:

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @staticmethod
    def get_user(faker):
        return {
            "username": faker.name(),
            "password": faker.password(),
            "email": faker.email()
        }