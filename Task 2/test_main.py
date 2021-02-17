from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as es

from parser_main import AvitoMainPage, AvitoSearchPage, AvitoAdPage, OrderingPage


class Test_Parser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        # self.driver = self.setup_settings()
        # Даю время на загрузку страниц перед продолжением
        self.driver.implicitly_wait(5)

        self.main_page = None
        self.search_page = None
        self.ad_page = None
        self.ordering_page = None

    @staticmethod
    def setup_settings():
        options = webdriver.ChromeOptions()
        options.add_argument(r"--user-data-dir=./Chrome_profile")
        return webdriver.Chrome(options)

    def test_main_page_loading(self):
        # Создаем инстанс авито мейн для (проверки) авторизации
        self.main_page = AvitoMainPage(self.driver)
        # Получаем фактический URL страницы на которой находимся и сверяем его с ожидаемым
        url = self.main_page.get_page_url()
        assert url == "https://www.avito.ru/sochi", \
            "Ошибка загрузки главной страницы Avito -> " + self.main_page.get_page_url()
        print("PASSED:\t Загрузка главной страницы " + url)

    def test_authorization(self):
        # Проверяем авторизирован ли уже пользователь, если нет - авторизируемся
        if self.main_page.check_authorization():
            self.main_page.log_in()

        # Проверяем наличие пункта ЛК в шапке - он есть только у авторизированного пользователя
        assert WebDriverWait(self.driver, 60).\
            until(es.visibility_of_element_located((By.XPATH, "//a[@data-marker = 'header/username-button']"))), \
            "Авторизация не выполненна"
        print("PASSED:\t Авторизация")

    def test_search_page_loading(self):
        # Создаем инстанс страницы поиска товаров. На ней выбираем одно и получаем его ссылку
        self.search_page = AvitoSearchPage(self.driver)
        url = self.search_page.get_page_url()
        assert url == "https://www.avito.ru/sochi/lichnye_veschi?cd=1&d=1", \
            "Ошибка загрузки страницы поиска товаров"
        print("PASSED:\t Загрузка страницы поиска товаров " + url)

    def test_ad_page(self):
        # Открываем страницу конкретного товара
        link = self.search_page.get_first_ad_link()
        self.ad_page = AvitoAdPage(self.driver, link)
        url = self.ad_page.get_page_url()
        assert r"https://www.avito.ru/sochi/" in url, \
            "Ошибка перехода на страницу товара"
        print("PASSED:\t Загрузка страницы товара " + url)

    def test_ordering_page(self):
        # Переходим на страницу заказа товара
        self.ad_page.go_to_ordering_page()
        # # Создаем инстанс страницы заказа
        self.ordering_page = OrderingPage(self.driver)
        # После нажатия кнопки, страница загружалась слишком быстро новые данные (URL) не успевали зафиксироваться
        # Добавил время ожидания до появления нового заголовка страницы
        WebDriverWait(self.driver, 10).until(es.title_is("Авито — Объявления на сайте Авито"))
        url = self.driver.current_url
        assert "https://www.avito.ru/order/checkout/" in url, \
            "Ошибка загрузки страницы заказа товара " + url
        print("PASSED:\t Загрузка страницы заказа " + url)

    def test_phone_field(self):

        # Получаем значения поля, в которое должен вводиться телефон
        phone_field_content = self.ordering_page.get_content_phone_field()

        assert phone_field_content == "", "Поле для ввода телефона не пустое, почему-то"
        print("PASSED:\t Поле ввода мобильного телефона пустое ")


if __name__ == '__main__':

    case = Test_Parser()

    # Загружаем и тестируем подгрузку главной страницы Avito
    case.test_main_page_loading()

    # Проверка авторизации на сайте
    case.test_authorization()

    # Проверка загрузки страницы поиска товаров
    case.test_search_page_loading()

    # Проверка открытия страницы товара
    case.test_ad_page()

    # Проверка страницы заказа товара
    case.test_ordering_page()

    # Проверка значения поля для ввода телефона. ожидается ""
    case.test_phone_field()

    # Закрываем drive
    case.driver.close()

    # Если не возникло ошибок в коде - все тесты выполненны верно
    print("Все тесты пройдены успешно")
