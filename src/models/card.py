from faker import Faker


class Card:

    def __init__(self, longNum, expires, ccv, userID):
        self.long_num = longNum
        self.expires = expires
        self.ccv = ccv
        self.user_id = userID

    @classmethod
    def from_faker(cls, user_id):
        data = {
            "longNum": Faker().credit_card_number(),
            "expires": Faker().credit_card_expire(),
            "ccv": Faker().credit_card_security_code(),
            "userID": user_id
        }
        return cls(**data)

    @property
    def card(self):
        return {
            "longNum": self.long_num,
            "expires": self.expires,
            "ccv": self.ccv,
            "userID": self.user_id
        }