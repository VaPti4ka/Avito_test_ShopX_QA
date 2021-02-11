import settings
import pytest
from selenium import webdriver


class PageParser:
    def __init__(self):
        self.driver = None
        self.start_url = r"https://avito.ru"
        self.test_page_url = r"https://www.avito.ru/sochi/lichnye_veschi?cd=1&d=1"

    def start_browser(self):
        self.driver = webdriver.Chrome()
        self.go_to_page(self.start_url)

        # Закрываем окно
        # self.driver.quit()

    def go_to_page(self, url):
        self.driver.get(url)


# Создаем экземляр класса парсера
test_elem = PageParser()
# Запускаем сессию браузера
test_elem.start_browser()

# Ищем страницу логина
log_button = test_elem.driver.find_element_by_class_name("header-services-menu-link-not-authenticated-3kAga")
# Нажимаем на него
log_button.click()
# Вводим логин
log_button.send_keys(settings.login)

# Ищем поле логина и нажимаем на него
log_field = test_elem.driver.find_element_by_name("login")
log_field.click()
# Вводим логин
log_field.send_keys(settings.login)

# Ищем поле пароля
pass_field = test_elem.driver.find_element_by_name("password")
pass_field.click()
# Вводим логин
pass_field.send_keys(settings.password)

# Ищем кнопку авторизации
test_elem.driver.find_element_by_class_name("auth-form-auth-form__submit-rSWaC").click()
