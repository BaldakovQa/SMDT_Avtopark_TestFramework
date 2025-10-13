import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.model_units import GenHandbookPage


def test_archive_model_unit(authorized_driver, created_model):
    page = GenHandbookPage(authorized_driver)
    page.archive_model_unit(created_model)
    assert not page.is_model_present(created_model), f"❌ Модель {created_model} всё ещё отображается"
    print(f"✅ Модель '{created_model}' успешно архивирована")

def test_open_models_archive(authorized_driver):
    """Тест: проверка открытия страницы с архивными моделями"""
    page = GenHandbookPage(authorized_driver)
    time.sleep(3)
    # Действие
    page.open_models_archive()
    time.sleep(3)
