import time

from pages.General_spravochniki.permissible_variations import PermissibleVariations,press_add_permission


def test_add_new_permissible_variations(authorized_driver):
    page = PermissibleVariations(authorized_driver)
    page.open_pemissible_variations()
    page.safe_click(press_add_permission)
    page.add_new_permission()

def test_archive_permission(authorized_driver):
    page = PermissibleVariations(authorized_driver)
    page.open_pemissible_variations()
    page.archive_permission()

def test_open_archive(authorized_driver):
    page = PermissibleVariations(authorized_driver)
    page.open_pemissible_variations()
    page.open_archive()
