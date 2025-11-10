from pages.General_spravochniki.models_sensors import ModelsSensors
import time

def test_add_models_sensors(authorized_driver):
    page = ModelsSensors(authorized_driver)
    page.open_models_sensors()
    page.press_add_models_sensor_button()
    page.fill_name_sensor_models_field()
    page.make_new_sensor_manufacturer()
    time.sleep(2)
    page.press_add_new_models_sensor_button()
    time.sleep(5)

def test_archive_models_sensors(authorized_driver):
    page = ModelsSensors(authorized_driver)
    page.open_models_sensors()
    page.archive_models_sensors()

def test_open_archive_models_sensors(authorized_driver):
    page = ModelsSensors(authorized_driver)
    page.open_models_sensors()
    page.open_models_sensors_archive()


