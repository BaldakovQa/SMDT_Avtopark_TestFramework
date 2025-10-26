import time
from pages.General_spravochniki.makers_sensors import MarkersSensor
from pages.General_spravochniki.makers_sensors import press_add_manufacturer_button



def test_add_new_manufacturer(authorized_driver):
    page = MarkersSensor(authorized_driver)
    page.open_markers_sensors()
    page.safe_click(press_add_manufacturer_button)
    page.add_new_sensors_manufacturer()


def test_archive_manufacturer(authorized_driver):
    page = MarkersSensor(authorized_driver)
    page.open_markers_sensors()
    page.archive_sensors_manufacturer()
    time.sleep(2)

def test_open_sensors_manufacturer_archive(authorized_driver):
    page = MarkersSensor(authorized_driver)
    page.open_markers_sensors()
    page.open_models_sensors_manufacturer_archive()
    time.sleep(2)