import random
import string
import time
from os import waitid

from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

add_equipments_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-vehicles-equips-equipments-header__left_btn']")

class Equipments:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/vehicles-equips/equipments")
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

    def open_equipments(self):
        self.driver.get(f"{Config.BASE_URL}/vehicles-equips/equipments")

    def equipments_name(self):
        length = random.randint(3, 7)
        name = ''.join(random.choices(string.ascii_uppercase, k=length))
        return name

    def add_new_equipments_all_empty(self, name=None):
        if name is None:
            name = self.equipments_name()
        wait = self.wait

        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите наименование оборудования']"))).send_keys(name)

        #Помещение
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow'])[3]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Гараж']//div[1]"))).click()

        #тип оборудования
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Стационарное']//div[1]"))).click()

        #орга владелец
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow'])[4]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-item ant-select-item-option ant-select-item-option-active']"))).click()

        #Статус
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='В гараже']//div[1]"))).click()

        #орга пользователь
        wait.until(EC.presence_of_element_located((By.XPATH,"//input[@id='addEquipment_organizationClient']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-item ant-select-item-option ant-select-item-option-active']"))).click()

        #Марка
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='addEquipment_equipmentBrand']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-item-option-content' and starts-with(text(), 'Имя')])[1]"))).click()

        #Ввод в эксплуатацию
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Выберите дату ввода в эксплуатацию']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ant-picker-today-btn']"))).click()

        #Модель
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='addEquipment_equipmentModel']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-item-option-content' and starts-with(text(), 'Имя')])[1]"))).click()

        #Гараж
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='addEquipment_garage']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-item-option-content' and contains(text(), 'гараж')])[2]"))).click()

        #Создаем
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary']"))).click()
        return name

    def archive_equipments(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-circle ant-btn-link ant-dropdown-trigger ant-btn-icon-only'])[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@role='menu']//span[contains(text(),'Архивировать')]"))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='archiveGarage_archiveDate']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ant-picker-today-btn']"))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-selector']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Списание']//div[1]"))).click()

        #Инпут файла в строку
        file_input = wait.until(EC.presence_of_element_located((By.ID, "archiveGarage_archiveFiles")))
        file_input.send_keys("/Users/anton/Downloads/shrek-shrek-forever-after-2010-2JD8HW6.jpg")
        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
