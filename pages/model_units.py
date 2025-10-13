import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from datetime import datetime
import time

class GenHandbookPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(f"{Config.BASE_URL}/directories/general")
        self.wait = WebDriverWait(driver, 15)

    def add_model_unit(self, model_name=None):
        wait = self.wait

        # ✅ Генерируем уникальное имя, если не передано
        if not model_name:
            model_name = f"TestUnitModel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        print(f"🧩 Используется имя модели: {model_name}")

        # Навигация по меню
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Справочники']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Общие справочники']"))).click()

        # Открываем выпадающий список
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-select-selection-item']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Модели агрегатов']"))).click()

        # Нажимаем "Добавить"
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'q-directories-general-units-models-header__left_btn')]")
        )).click()

        # Заполняем поля
        wait.until(EC.presence_of_element_located((By.ID, "addUnitModel_name"))).send_keys(model_name)
        wait.until(EC.presence_of_element_located((By.ID, "addUnitModel_type"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Двигатель']"))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='addUnitModel_engineType']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Бензиновый']//div[1]"))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='addUnitModel_enginePower']"))).send_keys("142")

        # Сохранение
        try:
            save_button = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[@class='ant-btn ant-btn-primary']//span[contains(text(),'Добавить')]"
            )))
            save_button.click()
            print("✅ Кнопка 'Добавить' нажата.")
        except Exception as e:
            print(f"⚠️ Кнопка 'Добавить' не найдена: {e}")

        # Проверка
        wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{model_name}')]")))
        print(f"✅ Модель агрегата '{model_name}' успешно добавлена!")

        return model_name  # ✅ возвращаем имя, чтобы можно было потом удалить

    def archive_model_unit(self, model_name):
        wait = self.wait
        # Переход в раздел Общие справочники
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Справочники']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Общие справочники']"))).click()
        # Открываем выпадающий список "Модели агрегатов"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-select-selection-item']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Модели агрегатов']"))).click()
        # Находим карточку нужной модели
        model_card = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(text(), '{model_name}')]/ancestor::div[contains(@class, 'ant-card')]")
        ))
        # Ждём, пока карточка станет видимой
        wait.until(EC.visibility_of(model_card))
        # Ищем кнопку "Архивировать" внутри карточки по уникальному атрибуту
        archive_btn = model_card.find_element(By.XPATH, "(//button[@class='ant-btn ant-btn-default q-directories-general-units-models-card-actions__button ant-btn-icon-only'])[2]")  # заменяем индекс
        archive_btn.click()
        # Подтверждаем архивирование в модальном окне
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='ant-btn ant-btn-primary'])[2]"))).click()
        print(f"✅ Модель '{model_name}' успешно отправлена в архив.")

    def is_model_present(self, model_name):
    #     """Проверяет, отображается ли модель в списке"""
        time.sleep(2)
        elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{model_name}')]")
        return len(elements) > 0

    def open_models_archive(self):
        wait = self.wait

        # Переход в раздел Общие справочники
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Справочники']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Общие справочники']"))).click()

        # Открываем выпадающий список "Модели агрегатов"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ant-select-selection-item']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Модели агрегатов']"))).click()

        time.sleep(3)  # немного подождать, пока таблица прогрузится

        # Открываем фильтры
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//button[contains(@class,'ant-btn-primary') and contains(.,'Фильтры')])[1]")
        )).click()

        # Кликаем по полю "Статус"
        wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='ant-select-selector'])[2]"))).click()

        # Выбираем значение "Архивный"
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Архивный']"))).click()

        # Нажимаем "Применить"
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Применить']]")
        )).click()

        time.sleep(3)
        print("✅ Мы на странице с архивными моделями")

