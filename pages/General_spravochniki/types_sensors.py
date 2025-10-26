from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
import time

add_types_sensors_button = (By.XPATH,"//button[@class='ant-btn ant-btn-primary q-directories-general-sensors-types-header__left_btn']")



class TypesSensors:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general")
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

    def open_types_sensors(self):
        driver = self.driver
        driver.get(f"{Config.BASE_URL}/directories/general/types-sensors")

    def add_types_sensors(self):
        wait = self.wait
        # Ждём появления кнопки "Добавить"
        button = wait.until(EC.element_to_be_clickable(add_types_sensors_button))
        button.click()

    def fill_types_sensors(self, sensors_types_name=None):
        if sensors_types_name is None:
            sensors_types_name = f"система{int(time.time())}"

        wait = self.wait

        # Заполнение формы
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите наименование вида датчика']"))).send_keys(sensors_types_name)
        # Ждем, пока пропадут всплывающие окна или таблица стабилизируется
        time.sleep(1)
        try:
            self.safe_click((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))
        except Exception as e:
            print(f"⚠️ Повторная попытка клика по кнопке сохранить: {e}")
            time.sleep(1)
            self.safe_click((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))
        return sensors_types_name

    def archive_types_sensors(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH,"(//button[@class='ant-btn ant-btn-default q-directories-general-sensors-types-card-actions__button ant-btn-icon-only'])[2]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        time.sleep(1)

    def open_types_sensors_archive(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//button[contains(@class,'ant-btn-primary') and contains(.,'Фильтры')])[1]"))).click()
        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()
        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архивный']"))).click()
        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Применить']]"))).click()
        time.sleep(3)