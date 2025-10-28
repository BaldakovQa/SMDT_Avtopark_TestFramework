import time

from pages.General_spravochniki.catalog_mulfunction import MalFunction, press_add_first_lvl_malfunction, press_add_second_lvl_malfunction


def test_add_new_first_lvl_malfunction(authorized_driver):
    page = MalFunction(authorized_driver)
    page.open_catalog_malfunction()
    page.safe_click(press_add_first_lvl_malfunction)
    page.add_new_first_lvl_malfunction()

def test_add_new_second_lvl_malfunction(authorized_driver):
    page = MalFunction(authorized_driver)
    page.open_catalog_malfunction()
    page.add_new_second_lvl_malfunction()
    time.sleep(4)

def test_archive_1st_lvl_malfunction(authorized_driver):
    page = MalFunction(authorized_driver)
    page.open_catalog_malfunction()
    page.archive_1st_lvl_malfunction()