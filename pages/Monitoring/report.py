import random
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

press_add_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary']")

class Report:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/monitoring/report")
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

    def open_reports(self):
        self.driver.get(f"{Config.BASE_URL}/monitoring/report")

    def make_new_report(self):
        wait = self.wait
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Выберите период с']"))).send_keys("12.10.2025", Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Выберите период по']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='ant-picker-today-btn'])[2]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary']"))).click()