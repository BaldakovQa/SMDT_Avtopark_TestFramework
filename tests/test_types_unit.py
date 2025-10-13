import time

from selenium.webdriver.common.by import By
from pages.types_units import HandbookPage
from selenium.webdriver.support import expected_conditions as EC

def test_add_types_unit(authorized_driver):
    page = HandbookPage(authorized_driver)
    page.go_to_types_units()

    page.wait.until(EC.text_to_be_present_in_element(
        (By.XPATH, "//div[@class='ant-select-selector']"),
        "Типы агрегатов"
    ))
    print("✅ Мы в разделе 'Типы агрегатов'")
    new_type = page.add_types_units()
    print(f"✅ Создан новый тип агрегата: {new_type}")

def test_archive_types_units(authorized_driver):
    page = HandbookPage(authorized_driver)
    page.go_to_types_units()
    page.archive_types_units()
    # authorized_driver.quit()

def test_open_types_archive(authorized_driver):
    page = HandbookPage(authorized_driver)
    page.go_to_types_units()
    page.open_types_archive()
    time.sleep(3)
