from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
import time


add_work_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-works-types-header__left_btn']")

class TypesWorks:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/types-works")
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

    def open_works(self):
        driver = self.driver
        driver.get(f"{Config.BASE_URL}/directories/general/types-works")

    def fill_types_info(self, works_types=None):
        if works_types is None:
            works_types = f"Тип работы{int(time.time())}"
        wait = self.wait
        wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@placeholder='Введите тип работы'])[2]"))).send_keys(works_types)
        wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='ant-select-selection-overflow'])[2]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='ТО']//div[1]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='ant-select-selection-overflow'])[2]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[3]"))).click()

        return works_types

    def archive_types_work(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-default q-directories-general-works-types-card-actions__button ant-btn-icon-only'])[3]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        time.sleep(1)

    def open_archive_types_work(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'ant-btn-primary') and contains(.,'Фильтры')])[1]"))).click()
        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()
        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архивный']"))).click()
        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Применить']]"))).click()
        time.sleep(3)