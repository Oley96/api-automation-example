import logging
import allure


class AssertableResponse(object):

    def __init__(self, response):
        logging.info(f"Request: url={response.request.url}, body={response.request.body}")
        logging.info(f"Response: status={response.status_code}, body={response.text}")
        self._response = response


    @allure.step("response should have {condition}")
    def should_have(self, condition):
        logging.info("About to check " + str(condition))
        condition.match(self._response)
        return self

    def json(self):
        return self._response.json()
