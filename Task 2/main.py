import settings
import pytest
from selenium import webdriver


class PageParser:

    def __init__(self):
        # Следующие настройки позволяют сохранять данные о пользователе
        # Это дает возможность авторизироваться один раз, в последующие попытки, при использовании тех же настроек,
        # пользователь уже будет находиться на сайте
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"--user-data-dir=./Chrome_profile")
        self.driver = webdriver.Chrome(options=self.options)

        self.start_url = r"https://avito.ru"
        self.test_page_url = r"https://www.avito.ru/sochi/lichnye_veschi?cd=1&d=1"

    def start_browser(self):
        self.go_to_page(self.start_url)

        # Кривенькая проверка на авторизацию, лучше придумать не удалось
        # Пытаемся найти поле авторизации
        log_in_field = self.driver.find_elements_by_class_name("header-services-menu-link-not-authenticated-3kAga")

        if len(log_in_field) != 0:
            self.log_in(log_in_field[0])

        # Закрываем окно
        # self.driver.quit()

    def go_to_page(self, url):
        self.driver.get(url)

    def log_in(self, login_field):
        # Ищем элемент для авторизации и переходим по нему
        login_field.click()

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


# Создаем экземляр класса парсера
test_elem = PageParser()
# Запускаем сессию браузера
test_elem.start_browser()

# Перешли на страницу с которой будем тестировать
test_elem.go_to_page(test_elem.test_page_url)

# TODO Сделать выборку по нескольким элементам
# # Получаем список подходящих объявлений
# ad_list = test_elem.driver.find_elements_by_class_name("iva-item-root-G3n7v")
# for ad in ad_list:
#     # Находим ссылку на страницу элемента
#     ad.find_element_by_class_name("link-link-39EVK")

# Находим элемент обьявления
ad = test_elem.driver.find_element_by_class_name("iva-item-root-G3n7v")
# Находим в нем элемент с ссылкой и получаем ее
next_link = ad.find_element_by_class_name("link-link-39EVK").get_attribute("href")

# Перешли на страницу заказа
test_elem.go_to_page(next_link)

# Нажимаем на кнопку "Купить с доставкой"
test_elem.driver.find_element_by_class_name("item-buyer-button-1-zak").click()

# Находим поле для ввода телефона
test_elem.driver.find_element_by_name("phone").click()
