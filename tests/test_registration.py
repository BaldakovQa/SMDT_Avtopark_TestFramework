import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.registration_page import RegPage
from config import Config

def test_success_registration(driver):
    """Проверка успешной регистрации нового пользователя"""
    page = RegPage(driver)
    page.registration()

    # Ждём, пока произойдёт редирект
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    current_url = driver.current_url

    assert "/dashboard" in current_url, f"❌ Не произошёл переход на dashboard, текущий URL: {current_url}"
    print("✅ Регистрация успешна и переход подтверждён")
