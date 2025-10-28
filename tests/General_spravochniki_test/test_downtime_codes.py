from pages.General_spravochniki.downtime_codes import DowntimeCodes, press_add_downtime_button


def test_add_downtime_codes_owner_issue(authorized_driver):
    page = DowntimeCodes(authorized_driver)
    page.open_downtime_codes()
    page.safe_click(press_add_downtime_button)
    page.add_new_downtime_code_owner_issue()

def test_add_new_downtime_codes_customer_issue(authorized_driver):
    page = DowntimeCodes(authorized_driver)
    page.open_downtime_codes()
    page.safe_click(press_add_downtime_button)
    page.add_new_downtime_code_customer_issue()


def test_download_info_pdf(authorized_driver):
    page = DowntimeCodes(authorized_driver)
    page.open_downtime_codes()
    page.download_pdf()

def test_download_info_excel(authorized_driver):
    page = DowntimeCodes(authorized_driver)
    page.open_downtime_codes()
    page.download_excel()

def test_download_info_csv(authorized_driver):
    page = DowntimeCodes(authorized_driver)
    page.open_downtime_codes()
    page.download_csv()


