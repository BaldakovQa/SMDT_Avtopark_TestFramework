import random
import string
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

press_add_addressees = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-contractors-addressees-header__left_btn']")

class Addressees:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/addressees")
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

    def open_addressees(self):
        self.driver.get(f"{Config.BASE_URL}/directories/general/addressees")

    def add_new_catalog_addressees(self, name=None,surname=None):
        if name is None:
            name = ''.join(random.choices(string.ascii_letters, k=6))
        if surname is None:
            surname = ''.join(random.choices(string.ascii_letters, k=6))
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите фамилию']"))).send_keys(name)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите имя']"))).send_keys(surname)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary']"))).click()
        return name, surname

    def archive_addresses(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH,"(//button[@class='ant-btn ant-btn-default q-directories-general-contractors-addressees-card-actions__button ant-btn-icon-only'])[3]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        time.sleep(1)

    def open_archive_addressees(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary']"))).click()
        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()
        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архивный']"))).click()
        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Применить']]"))).click()
        time.sleep(3)

    def download_pdf(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-default q-button-export ant-dropdown-trigger']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='ant-dropdown-menu-title-content'])[1]"))).click()
        time.sleep(3)

    def download_excel(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-default q-button-export ant-dropdown-trigger']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='ant-dropdown-menu-title-content'])[2]"))).click()
        time.sleep(3)

    def download_csv(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-default q-button-export ant-dropdown-trigger']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='ant-dropdown-menu-title-content'])[3]"))).click()
        time.sleep(3)