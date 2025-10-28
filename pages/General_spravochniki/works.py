from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
import time


press_add_work_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-works-header__left_btn']")

class Works:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/works")
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

    def open_works(self):
        driver = self.driver
        driver.get(f"{Config.BASE_URL}/directories/general/works")

    def add_new_works(self, work=None):
        if work is None:
            work = f"Работа_{int(time.time())}"
        wait = self.wait

        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите наименование работы']"))).send_keys(work)
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='addWork_objectType']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='Транспортное средство']//div[1]"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='ant-select ant-select-in-form-item q-form-item__field ant-select-multiple ant-select-show-arrow ant-select-show-search']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='ТО']//div[1]"))).click()

            # Обработка типа работы
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-activedescendant='addWork_type_list_0']")))
            while True:
                try:
                    element.click()
                    break
                except StaleElementReferenceException:
                    element = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//input[@aria-activedescendant='addWork_type_list_0']")))

            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='Ремонт электрооборудования']//div[1]"))).click()

        except StaleElementReferenceException:
            # Перезапуск поиска элементов
            return self.add_new_works(work)


        ##Вторая часть, где мы заполняем "Тип ТС", "Нормочасы" и "стоямость часа"
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='addWork_types_0_vehicleType']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "// div[@title = 'Другие грузовики'] // div[1]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder ='Введите нормо-часы']"))).send_keys("2")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder ='Введите стоимость часа']"))).send_keys("1000")

        #СОзраняем результат
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class ='ant-btn ant-btn-primary']"))).click()
        return work


    def open_works_archive(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'ant-btn-primary') and contains(.,'Фильтры')])[1]"))).click()
        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()
        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архивный']"))).click()
        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Применить']]"))).click()
        time.sleep(3)