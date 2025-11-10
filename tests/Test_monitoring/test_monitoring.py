import time

from pages.Monitoring.report import Report,press_add_button

def test_make_new_report(authorized_driver):
    page = Report(authorized_driver)
    page.open_reports()
    page.safe_click(press_add_button)
    page.make_new_report()
    time.sleep(3)