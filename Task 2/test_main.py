import pytest
from selenium import webdriver
from parser_main import Page, AvitoMainPage, AvitoSearchPage, AvitoAdPage


class ParserTest:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.driver = self.setup_settings()
        self.driver.implicitly_wait(20)

        self.main_page = None
        self.search_page = None
        self.order_page = None

    def setup_settings(self):
        self.options.add_argument(r"--user-data-dir=./Chrome_profile")
        return webdriver.Chrome(options=self.options)

    def test_phone_field(self):
        # Создаем инстанс авито мейн для (проверки) авторизации
        self.main_page = AvitoMainPage(self.driver)

        # Проверка авторизации на сайте
        # Выполненна немного криво - по поиску поля авторизации
        if self.main_page.check_authorization():
            self.main_page.log_in()

        # Создаем инстанс страницы поиска товаров. На ней выбираем одно и получаем его ссылку
        self.search_page = AvitoSearchPage(self.driver)

        # Передаем найденную ссылку для создания инстанса страницы товара
        self.order_page = AvitoAdPage(self.driver, link=self.search_page.get_first_ad_link())


case = ParserTest()
case.test_phone_field()
