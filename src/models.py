
def get_user(faker):
    return {
        "username": faker.name(),
        "password": faker.password(),
        "email": faker.email()
    }

def get_card(faker, id):
    return {
        "longNum": faker.credit_card_number(),
        "expires": faker.credit_card_expire(),
        "ccv": faker.credit_card_security_code(),
        "userID": id
    }