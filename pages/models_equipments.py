from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from datetime import datetime
import time

class ModelsEquipments:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general")
        self.wait = WebDriverWait(driver, 15)

    def go_to_models_equipment(self):
        wait = self.wait
        # Переход в раздел Общие справочники
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Справочники']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Общие справочники']"))).click()
        #выбор справочника
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-select-selection-item']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Модель оборудования']"))).click()

    def add_equip_model(self, equip_model_name=None):
        wait = self.wait
        # Генерируем имя, если не передано
        if equip_model_name is None:
            equip_model_name = f"Имя Модели_{int(time.time())}"

            #Клик на кнопку добавить
            wait.until(EC.element_to_be_clickable(
                (By.XPATH,
                 "//button[@class='ant-btn ant-btn-primary q-directories-general-equipments-models-header__left_btn']")
            )).click()

            #Ввод инфы о модели в поле
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите наименование модели']"))).send_keys(equip_model_name)
            #добавление марки
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'+ Добавить марку оборудования')]"))).click()
            time.sleep(1)
            #Наименование марки
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@class='ant-input'])[2]"))).send_keys(equip_model_name)
            #Тип оборудования
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select ant-select-in-form-item ant-select-single ant-select-show-arrow']"))).click()
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Стационарное']//div[1]"))).click()
            #Клик на кнопку
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-space ant-space-horizontal ant-space-align-center']//div[1]//button[1]"))).click()
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-space ant-space-horizontal ant-space-align-center']//div[1]//button[1]"))).click()

        return equip_model_name

    def archive_equip_model(self):
        wait = self.wait
        # Находим кнопку архивирования внутри карточки
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'q-directories-general-equipments-models-card-actions__button')])[3]"))).click()
        time.sleep(1)
        #подтверждаем архивирование
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        time.sleep(1)

    def open_archive_model(self):
        wait = self.wait


        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//button[contains(@class,'ant-btn-primary') and contains(.,'Фильтры')])[1]")
        )).click()

        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()

        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архив']"))).click()

        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Применить']]")
        )).click()
        print("✅Мыв архиве")