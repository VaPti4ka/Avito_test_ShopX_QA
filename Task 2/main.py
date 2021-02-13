import settings
import pytest
from selenium import webdriver
from selenium.webdriver.common import By


class Page:

    def __init__(self):
        # Настройка использования профиля Chrome`a
        self.options = webdriver.ChromeOptions()
        self.driver = self.setup_settings()

        # self.test_page_url = r"https://www.avito.ru/sochi/lichnye_veschi?cd=1&d=1"

    def setup_settings(self):
        self.options.add_argument(r"--user-data-dir=./Chrome_profile")
        return webdriver.Chrome(options=self.options)

    def load_page(self, page_url):
        self.driver.get(page_url)

    def search_elem(self, locator):
        return self.driver.find_element(locator)


class AvitoMainPage(Page):
    LOGIN_ELEM = (By.XPATH, "//div/a[text()='Вход и регистрация']")
    LOGIN_FIELD = (By.Name, "login")
    PASSWORD_FIELD = (By.Name, "password")

    def __init__(self, driver=webdriver.Chrome):
        super().__init__()
        self.driver = driver
        self.link = r"https://avito.ru"

        # При создании инстанса класса сразу переходим на мейн страницу
        self.load_page(self.link)

    def log_in(self):
        self.search_elem(self.LOGIN_ELEM).click()

        login_field = self.search_elem(self.LOGIN_FIELD)
        login_field.click()
        login_field.send_keys(settings.login)

        pass_field = self.search_elem(self.PASSWORD_FIELD)
        pass_field.click()
        pass_field.send_keys(settings.password)
