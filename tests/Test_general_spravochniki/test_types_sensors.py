from pages.General_spravochniki.types_sensors import TypesSensors
import time


def test_add_types_sensors(authorized_driver):
    page = TypesSensors(authorized_driver)
    page.open_types_sensors()
    page.add_types_sensors()
    page.fill_types_sensors()
    print("✅Создано")

def test_archive_types_sensors(authorized_driver):
    page = TypesSensors(authorized_driver)
    page.open_types_sensors()
    page.archive_types_sensors()
    print("✅Архивация успешна")

def test_open_types_sensors_archive(authorized_driver):
    page = TypesSensors(authorized_driver)
    page.open_types_sensors()
    page.open_types_sensors_archive()
    print("\n✅Мы в архиве")
