import time

from pages.Special_spravochniki.units import Units, press_add_button

def test_add_new_unit(authorized_driver):
    page = Units(authorized_driver)
    page.open_units()
    page.safe_click(press_add_button)
    page.add_new_unit()

def test_archive_unit(authorized_driver):
    page = Units(authorized_driver)
    page.open_units()
    page.archive_unit()

def test_open_units_archive(authorized_driver):
    page = Units(authorized_driver)
    page.open_units()
    page.open_units_archive()
    time.sleep(3)