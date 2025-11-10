import time
from pages.General_spravochniki.types_works import TypesWorks, add_work_button


def test_add_new_types_Works(authorized_driver):
    page = TypesWorks(authorized_driver)
    page.open_works()
    page.safe_click(add_work_button)
    page.fill_types_info()
    time.sleep(2)

def test_archive_types_works(authorized_driver):
    page = TypesWorks(authorized_driver)
    page.open_works()
    page.archive_types_work()
    time.sleep(2)

def test_open_archive_types_work(authorized_driver):
    page = TypesWorks(authorized_driver)
    page.open_works()
    page.open_archive_types_work()
    time.sleep(2)
