import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

press_add_item_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-checklists-header__left_btn']")

class ItemChecklists:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/items-checklists")
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

    def open_items_checklists(self):
        self.driver.get(f"{Config.BASE_URL}/directories/general/items-checklists")

    def add_new_item(self, item=None):
        if item is None:
            item = f"Пункт_{int(time.time())}"
            wait = self.wait
            #Название
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Введите название']"))).send_keys(item)
            #Тип
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='addCheckListsListItem_type']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='ТС']//div[1]"))).click()
            #Формат
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='addCheckListsListItem_format']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='Строковое поле']//div[1]"))).click()
            #Добавить
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
            return item

    def archive_item(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-link ant-dropdown-trigger ant-btn-icon-only'])[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@role='menu']//span[contains(text(),'Архивировать')]"))).click()

    def open_archive_items(self):
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

    def download_pdf(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-default q-button-export ant-dropdown-trigger']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='ant-dropdown-menu-title-content'])[1]"))).click()
        time.sleep(3)

    def download_excel(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-default q-button-export ant-dropdown-trigger']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='ant-dropdown-menu-title-content'])[2]"))).click()
        time.sleep(3)

    def download_csv(self):
        wait = self.wait
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-default q-button-export ant-dropdown-trigger']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='ant-dropdown-menu-title-content'])[3]"))).click()
        time.sleep(3)

