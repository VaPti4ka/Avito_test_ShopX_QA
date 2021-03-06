import settings
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


class Page:

    def __init__(self, driver):
        self.driver = driver

    def load_page(self, page_url):
        self.driver.get(page_url)

    def search_elem(self, locator):
        return self.driver.find_element(*locator)

    def get_page_url(self):
        return self.driver.current_url

    def press_elem(self, locator):
        elem = self.driver.find_element(*locator)
        elem.click()
        return elem


class AvitoMainPage(Page):
    LOGIN_ELEM = (By.XPATH, "//a[text()='Вход и регистрация']")
    LOGIN_FIELD = (By.NAME, "login")
    LOGIN_BUTTON = (By.XPATH, "//button[@data-marker = 'login-form/submit']")
    PASSWORD_FIELD = (By.NAME, "password")

    def __init__(self, driver):
        super().__init__(driver)
        self.link = r"https://avito.ru/sochi"

        # При создании инстанса класса сразу переходим на мейн страницу
        self.load_page(self.link)

    def log_in(self):
        self.press_elem(self.LOGIN_ELEM)

        login_field = self.press_elem(self.LOGIN_FIELD)
        login_field.send_keys(settings.login)

        pass_field = self.press_elem(self.PASSWORD_FIELD)
        pass_field.send_keys(settings.password)

        self.press_elem(self.LOGIN_BUTTON)

    def check_authorization(self):
        # Возвращает 1, если поле для входа было найдено => необходимо авторизироваться
        # Возвращает 0, если авторизация уже пройдена
        try:
            self.search_elem(self.LOGIN_ELEM)
            return 1
        except:
            return 0


class AvitoSearchPage(Page):
    AD_ELEM = (By.XPATH, "//div/a[@data-marker='item-title']")

    def __init__(self, driver):
        super().__init__(driver)
        self.link = r"https://www.avito.ru/sochi/lichnye_veschi?cd=1&d=1"

        self.load_page(self.link)

    def get_first_ad_link(self):
        ad_elem = self.search_elem(self.AD_ELEM)
        link_to_item_page = ad_elem.get_attribute('href')
        return link_to_item_page


class AvitoAdPage(Page):
    ORDERING_BUTTON_ELEM = (By.XPATH, "//button[@data-marker = 'delivery-item-button-main']")

    def __init__(self, driver, link):
        super().__init__(driver)
        self.link = link

        self.load_page(self.link)

    def go_to_ordering_page(self):
        self.press_elem(self.ORDERING_BUTTON_ELEM)


class OrderingPage(Page):
    PHONE_FIELD_ELEM = (By.XPATH, "//input[@data-marker = 'sd/order-widget-field/phone']")

    def __init__(self, driver):
        super().__init__(driver)

    def get_content_phone_field(self):
        phone_field = self.search_elem(self.PHONE_FIELD_ELEM)
        return phone_field.get_attribute("value")
