import time

from pages.Special_spravochniki.tires import Tires, press_add_button


def test_add_new_tires(authorized_driver):
    page = Tires(authorized_driver)
    page.open_tires()
    page.safe_click(press_add_button)
    page.add_new_tire_make_marks()
    time.sleep(5)