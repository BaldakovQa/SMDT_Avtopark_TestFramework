from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from datetime import datetime
import time


class HandbookPage:
    def __init__(self, driver: object) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(f"{Config.BASE_URL}/directories/general")

    def go_to_types_units(self):
        wait = self.wait
        # Переход в раздел Общие справочники
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Справочники']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Общие справочники']"))).click()
        #выбор справочника
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-select-selection-item']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Типы агрегатов']"))).click()

    def add_types_units(self, types_name=None):
        wait = self.wait
        # Генерируем имя, если не передано
        if types_name is None:
            types_name = f"Агрегат_{int(time.time())}"

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-units-types-header__left_btn']")
        )).click()
        # Вводим имя типа
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@placeholder='Введите наименование типа агрегата']")
        )).send_keys(types_name)

        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]")
        )).click()
        return types_name

    def archive_types_units(self):
        wait = self.wait

        # Кликаем по первому чекбоксу
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='ant-checkbox'])[1]"))).click()

        # Кликаем по кнопке "Архивировать"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Архивировать')]"))).click()
        print("✅ Первый элемент успешно архивирован.")

    def open_types_archive(self):
        wait = self.wait

        filter_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//button[contains(@class,'ant-btn-primary') and contains(.,'Фильтры')])[1]")
        ))
        actions = ActionChains(self.driver)
        actions.move_to_element(filter_button).pause(0.2).click().perform()
        print("✅ Кнопка 'Фильтры' кликнута.")

        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()

        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архивный']"))).click()

        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Применить']]")
        )).click()





