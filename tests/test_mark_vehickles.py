import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.marks_vehicles import MarksVehicle

def test_add_mark_vehicle(authorized_driver):
    page = MarksVehicle(authorized_driver)
    page.open_marks_vehicles()
    print("✅ Мы в справочнике")
    page.press_add_button().click()
    print("✅ кнопка нажата")
    page.fill_marks_vehicle()
    print("✅ Элемент справочника создан")

def test_archive_marks_vehicles(authorized_driver):
    page = MarksVehicle(authorized_driver)
    page.open_marks_vehicles()
    print("✅ Мы в справочнике")
    page.press_archive_button()
    page.archive_marks_vehicles()
    print("✅ Модель в архиве")

def test_open_archive_marks_vehicles(authorized_driver):
    page = MarksVehicle(authorized_driver)
    page.open_marks_vehicles()
    print("✅ Мы в справочнике")
    page.open_archive_marks_vehicles()
    print("✅ Мы на странице с архивными марками")