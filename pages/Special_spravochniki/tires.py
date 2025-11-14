import random
import string
import time
from os import wait3

from selenium.common import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from config import Config
import random, string, time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

press_add_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-tires-header__left_btn']")
archive_first_tire = (By.XPATH, "(//button[@class='ant-btn ant-btn-default q-directories-garages-card-actions__button ant-btn-icon-only'])[3]")

class Tires:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/tires")
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

    def open_tires(self):
        self.driver.get(f"{Config.BASE_URL}/directories/tires")

    def add_new_tire_make_marks(self, name=None):


        if name is None:
            name = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))

        wait = self.wait
        driver = self.driver

        # === Добавляем марку ===
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Добавить марку')]"))).click()

        # === Вводим наименование ===
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Введите наименование марки шины']"))
        ).send_keys(name)

        # === Кликаем "Добавить" в модалке марки ===
        add_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "(//button[contains(@class, 'ant-btn-primary')]//span[contains(text(),'Добавить')])[1]"
        )))
        driver.execute_script("arguments[0].click();", add_button)

        # === Ждём закрытия модалки ===
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal__header")))

        # === Заполняем основные поля ===
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите норму пробега']"))).send_keys(
            "500000")
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите минимальный остаток']"))).send_keys(
            "0.5")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите пробег']"))).send_keys("0")

        # === Сохраняем ===
        save_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "(//button[contains(@class, 'q-directories-tires-form__button')])[2]"
        )))
        driver.execute_script("arguments[0].click();", save_button)

        # === Добавляем модель ===
        model_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Добавить модель')]")))
        driver.execute_script("arguments[0].click();", model_btn)

        # === Проверяем, открылась ли модалка модели ===
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Введите наименование модели шины']")
            ))
        except TimeoutException:
            print("⚠️ Модалка модели не открылась — проверяй интерфейс.")
            return

        # === Выбираем бренд в селекте ===
        try:
            select = wait.until(EC.element_to_be_clickable((
                By.XPATH, "(//div[contains(@class,'ant-select')]//div[@class='ant-select-selector'])[13]"
            )))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", select)
            time.sleep(0.5)

            try:
                ActionChains(driver).move_to_element(select).click().perform()
            except Exception:
                driver.execute_script("""
                    var elem = arguments[0];
                    var evt = new MouseEvent('mousedown', {bubbles: true});
                    elem.dispatchEvent(evt);
                """, select)
                print("⚠️ Пришлось использовать mousedown для открытия селекта")
        except TimeoutException:
            print("❌ Не найден селект бренда модели — возможно, изменился XPATH.")
            return

        # === Кликаем по первому элементу выпадающего списка ===
        option = wait.until(EC.element_to_be_clickable((
            By.XPATH, "(//div[contains(@class,'ant-select-item-option-content')])[1]"
        )))
        driver.execute_script("arguments[0].click();", option)
        print(f"✅ Марка '{name}' успешно добавлена и выбрана в модели.")

        # === Вводим наименование модели ===
        wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@placeholder='Введите наименование модели шины']"
        ))).send_keys(f"Шина_{name}")

        # === Кликаем по кнопке "Добавить" внутри модалки модели ===
        try:
            modal = wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class, 'ant-modal') and not(contains(@class,'hidden'))]"
            )))
            add_btn = modal.find_element(
                By.XPATH,
                ".//button[.//span[normalize-space(text())='Добавить'] and not(@disabled)]"
            )

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
            time.sleep(0.5)

            try:
                add_btn.click()
                print("✅ Обычный клик по кнопке 'Добавить' сработал.")
            except Exception:
                driver.execute_script("arguments[0].click();", add_btn)
                print("⚠️ JS-клик по кнопке 'Добавить' выполнен вместо обычного.")

        except TimeoutException:
            print("❌ Кнопка 'Добавить' для модели не найдена или неактивна.")
        except Exception as e:
            print(f"❌ Ошибка при клике по кнопке 'Добавить': {e}")
            driver.save_screenshot("debug_add_button.png")

        wait.until(EC.presence_of_element_located((By.ID, "addTire_type"))).click()

        return name


