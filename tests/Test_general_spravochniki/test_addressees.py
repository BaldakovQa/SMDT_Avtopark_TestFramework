from pages.General_spravochniki.addressees import Addressees, press_add_addressees

def test_add_new_address(authorized_driver):
    page = Addressees(authorized_driver)
    page.open_addressees()
    page.safe_click(press_add_addressees)
    page.add_new_catalog_addressees()

def test_archive_addresses(authorized_driver):
    page = Addressees(authorized_driver)
    page.open_addressees()
    page.archive_addresses()

def test_archive_marks_vehicles(authorized_driver):
    page = Addressees(authorized_driver)
    page.open_addressees()
    page.open_archive_addressees()

def test_download_files(authorized_driver):
    page = Addressees(authorized_driver)
    page.open_addressees()
    page.download_csv()
    page.download_pdf()
    page.download_excel()