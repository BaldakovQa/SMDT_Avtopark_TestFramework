import random
import string
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

press_add_user_pos = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-users-header__left_btn']")

class UserPos:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/users-positions")
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

    def open_user_positions(self):
        self.driver.get(f"{Config.BASE_URL}/directories/general/users-positions")

    def add_new_position(self, position=None):
        if position is None:
            random_part = ''.join(random.choices(string.ascii_letters, k=6))
            position = f"{random_part}"
            wait = self.wait
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите название']"))).send_keys(position)
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        return position

    def delete_user_position(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-link ant-dropdown-trigger ant-btn-icon-only'])[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-link q-directories-general-users-positions-table__menu_btn'])[2]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()


