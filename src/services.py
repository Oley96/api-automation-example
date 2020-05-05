import base64
import json
import os

import allure
import dotenv
import jsonpath_rw
import requests

from src.response import AssertableResponse


class ApiService(object):

    def __init__(self):
        dotenv.load_dotenv()
        self._base_url = os.getenv('BASE_URL')
        self._headers = {"content-type": "application/json"}

    def _post(self, url, body, cookies=None):
        if not cookies:
            cookies = {}
        return requests.post(f"{self._base_url}{url}", data=json.dumps(body),
                             headers=self._headers, cookies=cookies)

    def _delete(self, url, cookies=None):
        if not cookies:
            cookies = {}
        return requests.delete(f"{self._base_url}{url}", cookies=cookies, headers=self._headers)

    def _get(self, url, cookies=None):
        if not cookies:
            cookies = {}
        return requests.get(f"{self._base_url}{url}", cookies=cookies, headers=self._headers)


class UserApiService(ApiService):

    def __init__(self):
        super().__init__()

    @allure.step
    def register_customer(self, user):
        return AssertableResponse(self._post("/register", user))

    @allure.step
    def login(self):
        return AssertableResponse(self._get("/login"))

    @allure.step
    def login_with(self, user):
        encoded = base64.b64encode(str(user["username"]+":"+user["password"]).encode('utf-8', errors = 'strict'))
        auth_header = {"Authorization": "Basic " + str(encoded, 'utf-8')}
        self._headers.update(**auth_header)
        return AssertableResponse(self._get("/login"))

    @allure.step
    def get_customers(self):
        return AssertableResponse(self._get("/customers"))

    @allure.step
    def get_customer(self, customer_id):
        return AssertableResponse(self._get(f"/customers/{customer_id}"))

    @allure.step
    def delete_customer(self, id):
        return AssertableResponse(self._delete(f"/customers/{id}"))

    @allure.step
    def get_cards(self):
        return AssertableResponse(self._get("/cards"))

    @allure.step
    def get_card(self, id):
        return AssertableResponse(self._get(f"/cards/{id}"))

    @allure.step
    def add_card(self, card):
        return AssertableResponse(self._post("/cards", card))

    @allure.step
    def delete_card(self, id):
        return AssertableResponse(self._delete(f"/card/{id}"))

    @allure.step
    def get_addresses(self):
        return AssertableResponse(self._get("/addresses"))

    @allure.step
    def get_address(self, id):
        return AssertableResponse(self._get(f"/addresses/{id}"))

    @allure.step
    def add_address(self, address):
        return AssertableResponse(self._post("/addresses", address))

    @allure.step
    def delete_address(self, id):
        return AssertableResponse(self._delete(f"/addresses/{id}"))


class CatalogueApiService(ApiService):

    def __init__(self):
        super(CatalogueApiService, self).__init__()

    @allure.step
    def get_all_products(self):
        return AssertableResponse(self._get("/catalogue"))

    @allure.step
    def get_featured_product(self, index):
        return self.get_all_products().json()[index - 1]

    @allure.step
    def count_all_products(self):
        return len(jsonpath_rw.parse("$..id").find(self.get_all_products().json()))

    @allure.step
    def get_product(self, product_id):
        return AssertableResponse(self._get(f"/catalogue/{product_id}"))

    @allure.step
    def get_products_count(self):
        return AssertableResponse(self._get("/catalogue/size"))

    @allure.step
    def get_tags(self):
        return AssertableResponse(self._get("/tags"))

