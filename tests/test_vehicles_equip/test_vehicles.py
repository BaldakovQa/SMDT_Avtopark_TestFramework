from pages.Vehicles_equip.vehicles import Vehicles, add_vehicles_button
import time

def test_add_new_vehicle(authorized_driver):
    page = Vehicles(authorized_driver)
    page.open_vehicles()
    page.safe_click(add_vehicles_button)
    page.add_sedan_car_with_new_type_and_model()
    time.sleep(2)

def test_archive_car(authorized_driver):
    page = Vehicles(authorized_driver)
    page.open_vehicles()
    page.archive_car()