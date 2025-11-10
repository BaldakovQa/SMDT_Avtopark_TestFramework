import random
import string
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

press_add_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-units-header__left_btn']")

class Units:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/units")
        self.wait = WebDriverWait(driver, 15)

    def safe_click(self, locator, retries=3):
        driver = self.driver
        wait = WebDriverWait(driver, 15)
        for attempt in range(retries):
            try:
                element = wait.until(EC.presence_of_element_located(locator))
                wait.until(lambda d: element.is_displayed() and element.is_enabled())
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                driver.execute_script("arguments[0].click();", element)
                return
            except StaleElementReferenceException:
                if attempt < retries - 1:
                    time.sleep(0.5)
                else:
                    raise
            except Exception as e:
                print(f"⚠️ Ошибка при клике {locator}: {e}")
                time.sleep(0.5)

    def open_units(self):
        self.driver.get(f"{Config.BASE_URL}/directories/units")

    def add_new_unit(self, number=None):
        if number is None:
            number = ''.join(random.choices(string.digits, k=6))
        wait = self.wait
        #Тип номерного агрегата
        wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Двигатель']//div[1]"))).click()

        #Статус
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='На складе']//div[1]"))).click()

        #номер
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите номер агрегата']"))).send_keys(number)

        #Склад
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[4]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@status='[object Object]']"))).click()

        #Модель агрегата
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[6]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-item ant-select-item-option ant-select-item-option-active']"))).click()

        #ggtovo
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary']"))).click()

        return number

    def archive_unit(self):
        wait = self.wait
        #начало архивации, выбор режима архиваци первого элемента
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-default q-directories-units-card-actions__button ant-btn-icon-only'])[3]"))).click()

        #Выбор даты
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-picker q-directories-units-archive__form-date']"))).click()
        wait.until(EC.element_to_be_clickable(((By.XPATH, "//a[@class='ant-picker-today-btn']")))).click()

        #Причина архивации
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-selector']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Продажа']//div[1]"))).click()

        #Файл
        file_input = wait.until(EC.presence_of_element_located((By.ID, "archiveUnit_files")))
        file_input.send_keys("/Users/anton/Downloads/shrek-shrek-forever-after-2010-2JD8HW6.jpg")
        time.sleep(2)

        #gotovo
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()

    def open_units_archive(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'ant-btn-primary') and contains(.,'Фильтры')])[1]"))).click()
        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()
        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архив']"))).click()
        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Применить']]"))).click()
