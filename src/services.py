import json
import os

import allure
import jsonpath_rw
import requests

from src.response import AssertableResponse


class ApiService(object):

    def __init__(self):
        self._base_url = os.environ['BASE_URL']
        self._headers = {"content-type": "application/json"}

    def _post(self, url, body, cookies=None):
        if not cookies:
            cookies = {}
        return requests.post(f"{self._base_url}{url}", data=json.dumps(body),
                             headers=self._headers, cookies=cookies)

    def _delete(self, url):
        return requests.delete(f"{self._base_url}{url}")

    def _get(self, url, cookies=None):
        if not cookies:
            cookies = {}
        return requests.get(f"{self._base_url}{url}", cookies=cookies)


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
    def get_customers(self):
        return AssertableResponse(self._get("/customers"))

    @allure.step
    def get_id(self, user):
        return AssertableResponse(self._post("/register", user)).json()['id']

    @allure.step
    def delete_customer_by_id(self, id):
        return AssertableResponse(self._delete(f"/customers/{id}"))

    @allure.step
    def get_addresses(self):
        return AssertableResponse(self._get("/addresses"))






class CatalogueApiService(ApiService):

    def __init__(self):
        super(CatalogueApiService, self).__init__()

    @allure.step
    def get_all_items(self):
        return AssertableResponse(self._get("/catalogue"))

    @allure.step
    def count_all_items(self):
        return len(jsonpath_rw.parse("$..id").find(self.get_all_items().json()))

    @allure.step
    def get_item_by_id(self, id):
        return AssertableResponse(self._get(f"/catalogue/{id}"))

    @allure.step
    def get_catalogue_size(self):
        return AssertableResponse(self._get("/catalogue/size"))

    @allure.step
    def get_tags(self):
        return AssertableResponse(self._get("/tags"))

    @allure.step
    def get_featured_item_id(self, index):
        return self.get_all_items().json()[index-1]['id']