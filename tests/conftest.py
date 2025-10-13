from datetime import datetime
from pages.model_units import GenHandbookPage
from pages.types_units import HandbookPage
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from config import Config

@pytest.fixture(scope="session")
def driver():
    """Инициализация Chrome на всё время тестовой сессии"""
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Включи для headless-режима
    service = Service()  # Укажите путь к chromedriver если нужно: Service('/path/to/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def authorized_driver(driver):
    """Открывает сайт и выполняет логин один раз за сессию"""
    login_page = LoginPage(driver)
    login_page.login(Config.USERNAME, Config.PASSWORD)
    # Проверяем успешный редирект
    assert "/dashboard" in driver.current_url, "❌ Авторизация не удалась"
    print("✅ Авторизация выполнена успешно!")
    yield driver

@pytest.fixture(scope="function")  # scope="function": новая уникальная модель для каждого теста
def model_name():
    """Генерирует уникальное имя модели с timestamp (например, TestUnitModel_20251006_222013)"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Формат: YYYYMMDD_HHMMSS
    model_name = f"TestUnitModel_{timestamp}"
    print(f"🧩 Используется имя модели: {model_name}")
    return model_name

@pytest.fixture(scope="module")  # scope можно: function, class, module, session
def model_name(authorized_driver):
    """Создаёт модель агрегата один раз на модуль тестов"""
    page = GenHandbookPage(authorized_driver)
    name = page.add_model_unit()
    yield name  # возвращаем имя модели в тест
    print(f"🧹 Удаляю модель {name} после теста")
    try:
        page.archive_model_unit(name)
    except Exception as e:
        print(f"⚠️ Не удалось удалить модель {name}: {e}")

@pytest.fixture
def created_model(authorized_driver):
    page = GenHandbookPage(authorized_driver)
    model_name = page.add_model_unit()  # создаём модель с уникальным именем
    yield model_name

@pytest.fixture
def created_types(authorized_driver):
    page = HandbookPage(authorized_driver)
    types_name = page.add_types_units()  # ✅ вызываем метод
    yield types_name
