from pages.General_spravochniki.fuel_cards import FuelCards
import time

def test_add_fuel_card(authorized_driver):
    page = FuelCards(authorized_driver)
    page.open_fuel_cards()
    page.press_add_button()
    page.fill_fuel_cards()
    print("✅ Passed")

def test_archive_fuel_card(authorized_driver):
    page = FuelCards(authorized_driver)
    page.open_fuel_cards()
    page.archive_fuel_card()
    time.sleep(1)

def test_open_archive_fuel_card(authorized_driver):
    page = FuelCards(authorized_driver)
    page.open_fuel_cards()
    page.open_archive_fuel_cards()