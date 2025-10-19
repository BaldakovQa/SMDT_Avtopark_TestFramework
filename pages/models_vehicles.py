from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from datetime import datetime
import time

class ModelsVehicles:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general")
        self.wait = WebDriverWait(driver, 15)

    def go_to_models_vehicles(self):
        wait = self.wait
        # Переход в раздел Общие справочники
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Справочники']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Общие справочники']"))).click()
        # выбор справочника
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-select-selection-item']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Модель транспортного средства']"))).click()

    def add_models_vehicle(self, vehicle_model=None):
        wait = self.wait
        if vehicle_model is None:
            vehicle_model = f"Модель_{int(time.time())}"

        # Нажимаем кнопку
        wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[@class='ant-btn ant-btn-primary q-directories-general-vehicles-models-header__left_btn']"
        ))).click()

        # Теперь вносим данные в модалке
        wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@placeholder='Введите наименование модели транспортного средства']"))).send_keys(vehicle_model)

        # Костылим выбор модели
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='addModel_make']"))).click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'ABG')]"))).click()

        # Костылим вид ТС
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-col ant-form-item-control'])[4]"))).click()
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@code='TRUCKS_AND_SPECIAL_VEHICLE']"))).click()

        #костылим Тип ТС
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='addModel_vehicleType']"))).click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Грузовики']//div[@class='ant-select-item-option-content'][contains(text(),'Мототехника')]"))).click()
        #Кликаем
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        return vehicle_model
