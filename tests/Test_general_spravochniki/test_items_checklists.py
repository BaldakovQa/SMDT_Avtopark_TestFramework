from pages.General_spravochniki.items_checklists import ItemChecklists,press_add_item_button
import time

def test_add_new_checklists(authorized_driver):
    page = ItemChecklists(authorized_driver)
    page.open_items_checklists()
    page.safe_click(press_add_item_button)
    page.add_new_item()
    time.sleep(1)

def test_archive_checklists_item(authorized_driver):
    page = ItemChecklists(authorized_driver)
    page.open_items_checklists()
    page.archive_item()
    time.sleep(2)

def test_open_archived_checklists_item(authorized_driver):
    page = ItemChecklists(authorized_driver)
    page.open_items_checklists()
    page.open_archive_items()

def test_download_info_pdf(authorized_driver):
    page = ItemChecklists(authorized_driver)
    page.open_items_checklists()
    page.download_pdf()

def test_download_info_excel(authorized_driver):
    page = ItemChecklists(authorized_driver)
    page.open_items_checklists()
    page.download_excel()

def test_download_info_csv(authorized_driver):
    page = ItemChecklists(authorized_driver)
    page.open_items_checklists()
    page.download_csv()
