import random
import string
import time
from os import wait3

from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

press_add_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-garages-header__left-btn']")
archive_first_garage = (By.XPATH, "(//button[@class='ant-btn ant-btn-default q-directories-garages-card-actions__button ant-btn-icon-only'])[3]")

class Garages:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/garages")
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

    def open_garages(self):
        self.driver.get(f"{Config.BASE_URL}/directories/garages")

    def add_new_garage(self, name=None):
        if name is None:
            name = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))

        wait = self.wait
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите название гаража']"))).send_keys(name)

        #Генерация случайного адреса
        regions = ["Приморский край"]
        districts = ["г. Владивосток"]
        settlements = ["г. Владивосток"]
        streets = ["ул. Пушкина", "ул. Ленина", "ул. Гагарина", "ул. Чехова", "ул. Молодежная"]

        region = random.choice(regions)
        district = random.choice(districts)
        settlement = random.choice(settlements)
        street = random.choice(streets)
        house = random.randint(1, 200)

        address = f"{region}, {district}, {settlement}, {street}, д. {house}"
        #Борьба с ГАРом
        address_select = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[1]")))
        address_select.click()
        # Находим input внутри открытого дропа
        address_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'ant-select-selection-search-input')]")))
        # Вводим адрес и подтверждаем Enter
        address_input.send_keys(address)
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ant-select-item-option-content']"))).click()

        wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='ant-select-selection-overflow'])[1]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ant-select-item-option-content']"))).click()

        add_garage=wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]")))
        add_garage.click()
        return name

    def archive_first_garage(self):
        wait = self.wait
        #Гараж для орги
        wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='ant-select ant-select-in-form-item ant-select-single ant-select-allow-clear ant-select-show-arrow'])[1]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='ant-select-item-option-content'])[1]"))).click()

        #Гараж для складов
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='archiveGarage_garageToStorage']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-item-option-content'])[1]"))).click()
