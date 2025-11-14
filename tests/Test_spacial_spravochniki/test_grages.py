import time

from pages.Special_spravochniki.garages import Garages,press_add_button,archive_first_garage

def test_add_new_garage(authorized_driver):
    page = Garages(authorized_driver)
    page.open_garages()
    page.safe_click(press_add_button)
    page.add_new_garage()

def test_archive_first_garage(authorized_driver):
    page = Garages(authorized_driver)
    page.open_garages()
    page.safe_click(archive_first_garage)
    page.archive_first_garage()
