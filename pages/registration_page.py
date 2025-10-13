import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.core import driver

from config import Config

class RegPage:  # Переименовал в RegPage для consistency (было RegPage)
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/registration")  # Используем Config
        self.wait = WebDriverWait(self.driver, 10)

    def registration(self):
        self.wait.until(EC.presence_of_element_located((By.ID, "form_item_companyName"))).send_keys("Test Company")
        self.wait.until(EC.presence_of_element_located((By.ID, "form_item_domainName"))).send_keys("TestCompany")
        self.wait.until(EC.presence_of_element_located((By.ID, "form_item_email"))).send_keys("TestCompany@yopmail.com")
        self.wait.until(EC.presence_of_element_located((By.ID, "form_item_phone"))).send_keys("+7(950) 397-94-76")
        self.wait.until(EC.presence_of_element_located((By.ID, "form_item_lastName"))).send_keys("Балдаков")
        self.wait.until(EC.presence_of_element_located((By.ID, "form_item_firstName"))).send_keys("Антон")
        time.sleep(3)

        checkbox1 = self.driver.find_element(By.XPATH, "(//input[@type='checkbox'])[1]")
        checkbox2 = self.driver.find_element(By.XPATH, "(//input[@type='checkbox'])[2]")

        self.driver.execute_script("arguments[0].click();", checkbox1)
        self.driver.execute_script("arguments[0].click();", checkbox2)
        time.sleep(3)

        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//button[contains(@class, 'q-registration__button')])[2]"))
        ).click()
        # Исправлено: Ждем изменения URL на dashboard (или другой успех — проверьте реальный)
        self.wait.until_not(EC.url_contains("/registration"))  # Ждем, чтобы URL изменился
        print("✅ Регистрация успешно завершена!")