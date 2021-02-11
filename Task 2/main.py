import settings
import pytest
from selenium import webdriver


class PageParser:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"--user-data-dir=./Chrome_profile")
        self.driver = webdriver.Chrome(options=self.options)
        self.start_url = r"https://avito.ru"
        self.test_page_url = r"https://www.avito.ru/sochi/lichnye_veschi?cd=1&d=1"

    def start_browser(self):
        # self.driver = webdriver.Chrome()
        self.go_to_page(self.start_url)

        self.log_in()
        # Закрываем окно
        # self.driver.quit()

    def go_to_page(self, url):
        self.driver.get(url)

    def log_in(self):
        # Ищем элемент для авторизации и переходим по нему
        self.driver.find_element_by_class_name("header-services-menu-link-not-authenticated-3kAga").click()

        # Находим поле ввода логина, кликаем, вводим логин
        log_field = self.driver.find_element_by_name("login")
        log_field.click()
        log_field.send_keys(settings.login)

        # Аналогичная операция для пароля
        pass_field = self.driver.find_element_by_name("password")
        pass_field.click()
        pass_field.send_keys(settings.password)

        # Ищем и нажимаем кнопку авторизации
        login_button = self.driver.find_element_by_class_name("auth-form-auth-form__submit-rSWaC")
        login_button.click()


# Использование учетной записи чтобы не надо было логиниться
# # ********************************************************************************************************************
# options = webdriver.ChromeOptions()
# options.add_argument(r"--user-data-dir=./Task 2/Chrome_profile")
# PATH = "/Users/yourPath/Desktop/chromedriver"
# driver = webdriver.Chrome(PATH, options=options)
# # ********************************************************************************************************************


# Создаем экземляр класса парсера
test_elem = PageParser()
# Запускаем сессию браузера
test_elem.start_browser()

# TODO Добавить проверку на авторизацию на сайте
# Логинимся
test_elem.log_in()

# Перешли на страницу с которой будем тестировать
test_elem.go_to_page(test_elem.test_page_url)
