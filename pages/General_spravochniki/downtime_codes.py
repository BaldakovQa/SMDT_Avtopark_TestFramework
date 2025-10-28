import random
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

press_add_downtime_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-downtime-codes-header__left_btn']")

class DowntimeCodes:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/downtime-codes")
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

    def open_downtime_codes(self):
        self.driver.get(f"{Config.BASE_URL}/directories/general/downtime-codes")

    def add_new_downtime_code_owner_issue(self, code_name=None, code_num=None):
        wait = self.wait
        if code_name is None:
            code_name = f"Код простоя{int(time.time())}"
        if code_num is None:
            code_num = random.randint(1, 10000)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите наименование простоя ']"))).send_keys(code_name)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//label[@class='ant-radio-button-wrapper ant-radio-button-wrapper-in-form-item'])[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите код простоя']"))).send_keys(str(code_num))
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()

        return code_name, code_num

    def add_new_downtime_code_customer_issue(self, code_name=None, code_num=None):
        wait = self.wait
        if code_name is None:
            code_name = f"Код простоя{int(time.time())}"
        if code_num is None:
            code_num = random.randint(1, 10000)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите наименование простоя ']"))).send_keys(code_name)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//label[@class='ant-radio-button-wrapper ant-radio-button-wrapper-in-form-item'])[2]"))).click()
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите код простоя']"))).send_keys(str(code_num))
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()


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