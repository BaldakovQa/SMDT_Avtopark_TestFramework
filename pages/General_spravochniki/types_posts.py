from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
import time


press_add_posts_button = (By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-service-posts-types-header__left_btn']")

class TypesPosts:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general/types-posts")
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

    def open_types_posts(self):
        driver = self.driver
        driver.get(f"{Config.BASE_URL}/directories/general/types-posts")


    def add_new_type_posts(self, posts_name=None):
        if  posts_name is None:
            posts_name = f"Пост ремонтный{int(time.time())}"
        wait = self.wait
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn ant-btn-primary q-directories-general-works-types-header__left_btn']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Введите тип рабочего поста']"))).send_keys(posts_name)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        return posts_name

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