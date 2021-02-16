import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from parser_main import Page, AvitoMainPage, AvitoSearchPage, AvitoAdPage, OrderingPage


class Test_Parser:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.driver = self.setup_settings()
        self.driver.implicitly_wait(5)

        self.main_page = None
        self.search_page = None
        self.ad_page = None
        self.ordering_page = None

    def setup_settings(self):
        self.options.add_argument(r"--user-data-dir=./Chrome_profile")
        return webdriver.Chrome(options=self.options)

    def test_main(self):
        # Загружаем и тестируем подгрузку главной страницы Avito
        self.test_main_page_loading()

        # Проверка авторизации на сайте
        self.test_authorization()

        # Проверка загрузки страницы поиска товаров
        self.test_search_page_loading()

        # Проверка открытия страницы товара
        self.test_ad_page()

        # Проверка страницы заказа товара
        self.test_ordering_page()

        # Проверка значения поля для ввода телефона. ожидается ""
        self.test_phone_field()

    def test_main_page_loading(self):
        # Создаем инстанс авито мейн для (проверки) авторизации
        self.main_page = AvitoMainPage(self.driver)
        # Получаем фактический URL страницы на которой находимся и сверяем его с ожидаемым
        assert self.main_page.get_page_url() == "https://www.avito.ru/sochi", \
            "Ошибка загрузки главной страницы Avito -> " + self.main_page.get_page_url()

    def test_authorization(self):
        # Проверяем авторизирован ли уже пользователь, если нет - авторизируемся
        if self.main_page.check_authorization():
            self.main_page.log_in()

        # Проверяем наличие пункта ЛК в шапке - он есть только у авторизированного пользователя
        assert self.main_page.search_elem([By.XPATH, "//a[@data-marker = 'header/username-button']"]), \
            "Авторизация не выполненна"

    def test_search_page_loading(self):
        # Создаем инстанс страницы поиска товаров. На ней выбираем одно и получаем его ссылку
        self.search_page = AvitoSearchPage(self.driver)
        assert self.search_page.get_page_url() == "https://www.avito.ru/sochi/lichnye_veschi?cd=1&d=1", \
            "Ошибка загрузки страницы поиска товаров"

    def test_ad_page(self):
        # Открываем страницу конкретного товара
        link = self.search_page.get_first_ad_link()
        self.ad_page = AvitoAdPage(self.driver, link)
        assert r"https://www.avito.ru/sochi/" in self.ad_page.get_page_url(),\
            "Ошибка перехода на страницу товара, текущая страница " + self.ad_page.get_page_url()

    def test_ordering_page(self):
        # Переходим на страницу заказа товара
        self.ad_page.go_to_ordering_page()
        # Создаем инстанс страницы заказа
        self.ordering_page = OrderingPage(self.driver)
        assert "https://www.avito.ru/order/checkout/" in self.ordering_page.get_page_url(), \
            "Ошибка загрузки страницы заказа товара"

    def test_phone_field(self):
        # Переходим дальше на страницу оформления заказа
        self.ordering_page = OrderingPage(self.driver)
        # Получаем значения поля, в которое должен вводиться телефон
        phone_field_content = self.ordering_page.get_content_phone_field()

        assert phone_field_content == "", "Поле для ввода телефона не пустое, почему-то"


case = Test_Parser()
case.test_main()
