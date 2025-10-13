from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/login")
        self.wait = WebDriverWait(self.driver, 10)

    def login(self, username=Config.USERNAME, password=Config.PASSWORD, expect_success=True):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(username)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(password)  # Исправлено: By.XPATH
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg q-login-form__button']"))).click()
        # Ждем успешного редиректа (предполагаем /dashboard — проверьте реальный)
        if expect_success:
            # ожидаем успешный переход
            self.wait.until(EC.url_contains("/dashboard"))
        else:
            # ожидаем, что останемся на странице логина
            self.wait.until(EC.url_contains("/login"))
