from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
import time

add_card_button = (By.XPATH,"//button[@class='ant-btn ant-btn-primary q-directories-general-vehicles-fuel-cards-header__left_btn']")



class FuelCards:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/fuel-cards")
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

    def open_fuel_cards(self):
        wait = self.wait
        driver = self.driver

        # Проверяем, находимся ли уже на странице справочника
        if "fuel-cards" not in driver.current_url:
            driver.get(f"{Config.BASE_URL}/directories/fuel-cards")
            # Переход в раздел "Справочники"
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Справочники']"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Общие справочники']"))).click()
            # Открываем выпадающий список
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-select-selection-item']"))).click()
            option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Топливные карты']")))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
            time.sleep(0.2)
            option.click()
        print("✅ Выбран справочник 'Топливные карты'")

    def press_add_button(self):
        wait = self.wait
        driver = self.driver
        try:
            button = wait.until(EC.presence_of_element_located(add_card_button))
            wait.until(EC.visibility_of(button))
            wait.until(EC.element_to_be_clickable(add_card_button))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
            return button
        except Exception as e:
            print("❌ Ошибка при нажатии кнопки 'Добавить':", e)
            raise

    def fill_fuel_cards(self, fuel_card_name=None):
        if fuel_card_name is None:
            fuel_card_name = f"Карта{int(time.time())}"

        wait = self.wait

        # Заполнение формы
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите номер топливной карты']"))).send_keys(fuel_card_name)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите наименование топливной карты']"))).send_keys("Карта топливная")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите кем выдана топливная карта']"))).send_keys("Роснефть")

        # Выбор даты
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Выберите дату выдачи топливной карты']"))).click()
        today_date_click_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='ant-picker-today-btn']")))
        today_date_click_btn.click()
        print("✅ Сегодняшняя дата выбрана")
        # Ждем, пока пропадут всплывающие окна или таблица стабилизируется
        time.sleep(1)
        try:
            self.safe_click((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))
        except Exception as e:
            print(f"⚠️ Повторная попытка клика по кнопке сохранить: {e}")
            time.sleep(1)
            self.safe_click((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))
        return fuel_card_name

    def archive_fuel_card(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-default q-directories-general-vehicles-fuel-cards-card-actions__button ant-btn-icon-only'])[3]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        time.sleep(1)

    def open_archive_fuel_cards(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'ant-btn-primary') and contains(.,'Фильтры')])[1]"))).click()
        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()
        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архивный']"))).click()
        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Применить']]"))).click()
        time.sleep(3)
