import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pages.models_equipments import ModelsEquipments
from selenium.webdriver.support import expected_conditions as EC

def test_add_types_unit(authorized_driver):
    page = ModelsEquipments(authorized_driver)
    page.go_to_models_equipment()
    page.add_equip_model()
    print("✅ Модель добавлена")


def test_archive_added_types_unit(authorized_driver):
    page = ModelsEquipments(authorized_driver)
    page.go_to_models_equipment()
    time.sleep(1)
    page.archive_equip_model()
    print("✅ Модель заархивирована")

def test_open_types_unit_archive(authorized_driver):
    page = ModelsEquipments(authorized_driver)
    page.go_to_models_equipment()
    page.open_archive_model()
    time.sleep(4)
    print("✅ Мы в архиве")
