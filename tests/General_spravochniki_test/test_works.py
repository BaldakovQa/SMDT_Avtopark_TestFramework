from pages.General_spravochniki.works import Works, press_add_work_button
import time

def test_add_new_works(authorized_driver):
    page = Works(authorized_driver)
    page.open_works()
    page.safe_click(press_add_work_button)
    page.add_new_works()
    time.sleep(5)

def test_open_archived_works(authorized_driver):
    page = Works(authorized_driver)
    page.open_works()
    page.open_works_archive()
    time.sleep(1)


#Баги в самом справочнике