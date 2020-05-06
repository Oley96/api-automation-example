rm -rf allure-results

mkdir -p allure-results

rm -rf allure-report

pytest ./tests

allure serve allure-results