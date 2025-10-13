import pytest
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

def test_login_success(driver):
    login_page = LoginPage(driver)
    login_page.login(Config.USERNAME, Config.PASSWORD)  # Используем Config
    # Исправлено: Ждем редиректа на dashboard
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    assert "/dashboard" in driver.current_url, "Логин  удался"

def test_login_failure(driver):
    login_page = LoginPage(driver)
    login_page.login("invalid@example.com", Config.PASSWORD, expect_success=False)
    assert "/login" in driver.current_url

def test_pwd_failure(driver):
    login_page = LoginPage(driver)
    login_page.login(Config.USERNAME, "wrong_password", expect_success=False)
    assert "/login" in driver.current_url

def test_empty_fields(driver):
    login_page = LoginPage(driver)
    login_page.login("", "", expect_success=False)
    assert "/login" in driver.current_url
