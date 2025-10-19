from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
import time

add_button = (By.XPATH, "//button[contains(., 'Добавить')]")
archive_button = (By.XPATH, "(//button[@class='ant-btn ant-btn-default q-directories-general-vehicles-marks-card-actions__button ant-btn-icon-only'])[3]")
filter_button = (By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[1]")

class MarksVehicle:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/marks-vehicles")
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

    def open_marks_vehicles(self):
        wait = self.wait
        driver = self.driver

        # Проверяем, находимся ли уже на странице справочника
        if "marks-vehicles" not in driver.current_url:
            driver.get(f"{Config.BASE_URL}/directories/general")

            # Переход в раздел "Справочники"
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Справочники']"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Общие справочники']"))).click()

            # Открываем выпадающий список
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-select-selection-item']"))).click()

            # Ждём появления дропдауна
            dropdown = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-select-dropdown')]"))
            )

            # Кликаем по пункту "Марка транспортного средства"
            option = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='Марка транспортного средства']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
            time.sleep(0.2)
            option.click()

        print("✅ Выбран справочник 'Марка транспортного средства'")

    def press_add_button(self):
        wait = self.wait
        driver = self.driver
        try:
            button = wait.until(EC.presence_of_element_located(add_button))
            wait.until(EC.visibility_of(button))
            wait.until(EC.element_to_be_clickable(add_button))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
            return button
        except Exception as e:
            print("❌ Ошибка при нажатии кнопки 'Добавить':", e)
            raise

    def press_filter_button(self):
        driver = self.driver
        wait = self.wait
        try:
            # Ждём, пока кнопка станет кликабельной
            button = wait.until(EC.element_to_be_clickable(filter_button))
            # JS-клик
            driver.execute_script("arguments[0].click();", button)
            # Небольшая пауза, чтобы Ant Design успел отрендерить форму
            time.sleep(0.3)
            # Ждём появления формы фильтра
            wait.until(EC.visibility_of_element_located((By.XPATH, "//form[contains(@class, 'ant-form')]")))
            return button
        except Exception as e:
            print("❌ Ошибка при нажатии кнопки 'Фильтр':", e)
            raise

    def press_archive_button(self):
        wait = self.wait
        driver = self.driver
        try:
            button = wait.until(EC.presence_of_element_located(archive_button))
            wait.until(EC.visibility_of(button))
            wait.until(EC.element_to_be_clickable(archive_button))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
            return button
        except Exception as e:
            print("❌ Ошибка при нажатии кнопки 'Архив':", e)
            raise

    def fill_marks_vehicle(self, mark_model_name=None):
        if mark_model_name is None:
            mark_model_name = f"Марка_{int(time.time())}"
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите наименование марки транспортного средства']"))).send_keys(mark_model_name)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        return mark_model_name

    def archive_marks_vehicles(self):
        wait = self.wait
        # Находим кнопку архивирования внутри карточки, она вынесена в константу
        time.sleep(1)
        #подтверждаем архивирование
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        time.sleep(1)

    def open_archive_marks_vehicles(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'ant-btn-primary') and contains(.,'Фильтры')])[1]"))).click()
        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()
        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архивный']"))).click()
        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Применить']]"))).click()
        time.sleep(3)