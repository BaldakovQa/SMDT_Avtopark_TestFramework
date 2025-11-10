import time

from pages.Vehicles_equip.equipments import Equipments,add_equipments_button


def test_add_new_equipments(authorized_driver):
    page = Equipments(authorized_driver)
    page.open_equipments()
    page.safe_click(add_equipments_button)
    page.add_new_equipments_all_empty()

def test_archive_equipments(authorized_driver):
    page = Equipments(authorized_driver)
    page.open_equipments()
    page.archive_equipments()
    time.sleep(2)
