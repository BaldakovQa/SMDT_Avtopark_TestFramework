from pages.General_spravochniki.types_posts import TypesPosts, press_add_posts_button


def test_add_types_posts(authorized_driver):
    page = TypesPosts(authorized_driver)
    page.open_types_posts()
    page.safe_click(press_add_posts_button)
    page.add_new_type_posts()

def test_download_info_pdf(authorized_driver):
    page = TypesPosts(authorized_driver)
    page.open_types_posts()
    page.download_pdf()

def test_download_info_excel(authorized_driver):
    page = TypesPosts(authorized_driver)
    page.open_types_posts()
    page.download_excel()

def test_download_info_csv(authorized_driver):
    page = TypesPosts(authorized_driver)
    page.open_types_posts()
    page.download_csv()


