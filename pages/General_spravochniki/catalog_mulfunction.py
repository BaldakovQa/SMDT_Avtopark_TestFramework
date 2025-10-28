import random
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

press_add_first_lvl_malfunction = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-catalog-malfunction-header__left_btn']")
press_add_second_lvl_malfunction = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-catalog-malfunction-header__left_btn']")

class MalFunction:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/catalog-malfunction")
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

    def open_catalog_malfunction(self):
        self.driver.get(f"{Config.BASE_URL}/directories/general/catalog-malfunction")

    def add_new_first_lvl_malfunction(self, mal_name=None):
        if mal_name is None:
            mal_name = f"Неисправность уровень 1{int(time.time())}"
            wait = self.wait
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите наименование неисправности']"))).send_keys(mal_name)
            wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
            return mal_name

    def add_new_second_lvl_malfunction(self, mal2_name=None):
        if mal2_name is None:
            mal2_name = f"Неисправность уровень 2{int(time.time())}"
            wait = self.wait
            wait.until(EC.presence_of_element_located((By.XPATH,"(//div[@class='ant-tabs-tab-btn'])[2]"))).click()
            self.safe_click(press_add_second_lvl_malfunction)
            wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@class='ant-select-selection-search-input'])[2]"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ant-select-item-option-content']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите наименование неисправности']"))).send_keys(mal2_name)
            wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
            return mal2_name

    def archive_1st_lvl_malfunction(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-default q-directories-general-catalog-malfunction-card-actions__button ant-btn-icon-only'])[3]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()

