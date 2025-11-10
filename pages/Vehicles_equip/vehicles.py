import random
import string
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

add_vehicles_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-vehicles-equips-vehicles-header__left_btn']")

class Vehicles:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/vehicles-equips/vehicles")
        self.wait = WebDriverWait(driver, 15)

    def safe_click(self, locator, retries=3):
        driver = self.driver
        wait = WebDriverWait(driver, 15)
        for attempt in range(retries):
            try:
                element = wait.until(EC.presence_of_element_located(locator))
                wait.until(lambda d: element.is_displayed() and element.is_enabled())
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                driver.execute_script("arguments[0].click();", element)
                return
            except StaleElementReferenceException:
                if attempt < retries - 1:
                    time.sleep(0.5)
                else:
                    raise
            except Exception as e:
                print(f"⚠️ Ошибка при клике {locator}: {e}")
                time.sleep(0.5)

    def open_vehicles(self):
        self.driver.get(f"{Config.BASE_URL}/vehicles-equips/vehicles")

    def random_grz(self):
        letters = "АВЕКМНОРСТУХ"  # русские буквы, похожие на латиницу
        region = str(random.choice([77, 78, 50, 99, 23, 161, 116, 138, 190, 196, 152]))  # популярные регионы РФ
        first_letter = random.choice(letters)
        middle_digits = ''.join(random.choices(string.digits, k=3))
        last_letters = ''.join(random.choices(letters, k=2))
        grz = f"{first_letter}{middle_digits}{last_letters}{region}"
        return grz

    def random_mark(self):
        length = random.randint(3, 7)
        mark = ''.join(random.choices(string.ascii_uppercase, k=length))
        return mark

    def random_model(self):
        length = random.randint(3, 7)
        model = ''.join(random.choices(string.ascii_uppercase, k=length))
        return model


    def random_vin(self):
        letters = ''.join(c for c in string.ascii_uppercase if c not in "IOQ")
        symbols = letters + string.digits
        vin = ''.join(random.choices(symbols, k=17))
        return vin

    def add_sedan_car_with_new_type_and_model(self,grz=None, vin=None, mark=None, model=None):
        if grz is None:
            grz = self.random_grz()
        if model is None:
            model = self.random_model()
        if mark is None:
            mark = self.random_mark()
        if vin is None:
            vin = self.random_vin()
        wait = self.wait
        #Основные
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите госномер']"))).send_keys(grz)

        #Создание марки
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-link q-vehicles-equips-vehicles-create-form__button'])[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите наименование марки транспортного средства']"))).send_keys(mark)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()

        #Создание модели
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-link q-vehicles-equips-vehicles-create-form__button'])[2]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите наименование модели транспортного средства']"))).send_keys(model)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='addModel_vehicleKind']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Автомобили']//div[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='addModel_vehicleType']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Легковые общего назначения']//div[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()

        #Продолжаем заполнять поля
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите начальный пробег']"))).send_keys("0")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Выберите дату ввода в эксплуатацию']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ant-picker-today-btn']"))).click()

        #Учетные данные
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='addVehicle_orgOwner']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-item-option-content']"))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='addVehicle_orgUser']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]"))).click()
        ###
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[4]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='В гараже']//div[1]"))).click()
        ###
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[6]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Грибочковый гараж']//div[1]"))).click()

        #Данные кузова
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите VIN или номер кузова']"))).send_keys(vin)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='ant-select-selector'])[7]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'TestUnitModel')]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='ant-switch-inner'])[6]"))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary']"))).click()
        return grz,vin,mark,model

    def archive_car(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-circle ant-btn-link ant-dropdown-trigger ant-btn-icon-only'])[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@role='menu']//span[contains(text(),'Архивировать')]"))).click()

        wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@id='archiveVehicle_date'])"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='ant-picker-now-btn'])"))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-selector']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Списание']//div[1]"))).click()

        #Инпут файла в строку
        file_input = wait.until(EC.presence_of_element_located((By.ID, "archiveVehicle_files")))
        file_input.send_keys("/Users/anton/Downloads/shrek-shrek-forever-after-2010-2JD8HW6.jpg")
        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])"))).click()
