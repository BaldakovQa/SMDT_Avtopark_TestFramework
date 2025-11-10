from pages.General_spravochniki.users_positions import UserPos, press_add_user_pos
import time

def test_add_new_position(authorized_driver):
    page = UserPos(authorized_driver)
    page.open_user_positions()
    page.safe_click(press_add_user_pos)
    position_name = page.add_new_position()



def test_delete_user_position(authorized_driver):
    page = UserPos(authorized_driver)
    page.open_user_positions()
    page.delete_user_position()