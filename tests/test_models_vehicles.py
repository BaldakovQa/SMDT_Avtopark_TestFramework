from pages.General_spravochniki.models_vehicles import ModelsVehicles
import time

def test_add_models_vehicles(authorized_driver):
    page = ModelsVehicles(authorized_driver)
    page.go_to_models_vehicles()
    print("✅ Мы перешли в раздел 'Модели транспортных средств'")
    page.add_models_vehicle("Test vehicle_model " + str(int(time.time())))
    time.sleep(2)
