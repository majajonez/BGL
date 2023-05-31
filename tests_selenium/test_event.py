from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from tests_selenium.fake_data import *

selenium = webdriver.Chrome()

event = Random_event()

def test_new_event():
    selenium.get('http://127.0.0.1:5000/auth/login')

    login_input = selenium.find_element(by=By.ID, value='username')
    password_input = selenium.find_element(by=By.ID, value='password')

    login_input.send_keys('maja')
    password_input.send_keys('123')

    button = selenium.find_element(by=By.XPATH, value="//input[@type='submit']")
    button.click()

    button_make_event = selenium.find_element(by=By.ID, value="button_make_event")
    button_make_event.click()

    title_input = selenium.find_element(by=By.ID, value='title')
    description_input = selenium.find_element(by=By.ID, value='description')
    when_input = selenium.find_element(by=By.ID, value='when')
    where_input = selenium.find_element(by=By.ID, value='where')
    seats_input = selenium.find_element(by=By.ID, value='the_number_of_seats')

    title_input.send_keys(event.title)
    description_input.send_keys(event.description)
    when_input.send_keys(event.when)
    where_input.send_keys(event.where)
    seats_input.send_keys(event.seats)

    button_confirm_event = selenium.find_element(by=By.XPATH, value="//input[@type='submit']")
    button_confirm_event.click()

    search_input = selenium.find_element(by=By.NAME, value='fraza')
    search_input.send_keys(event.title)

    game_button = selenium.find_element(by=By.XPATH, value="//input[@type='radio' and @value='gra']")
    selenium.execute_script("arguments[0].checked = true;", game_button)

    button_search = selenium.find_element(by=By.ID, value="button_search")
    button_search.click()

    join_button = selenium.find_element(by=By.ID, value="button_join")
    assert join_button.is_displayed()


def test_ev_details():
    selenium.get('http://127.0.0.1:5000/auth/login')

    login_input = selenium.find_element(by=By.ID, value='username')
    password_input = selenium.find_element(by=By.ID, value='password')

    login_input.send_keys('maja')
    password_input.send_keys('123')

    button = selenium.find_element(by=By.XPATH, value="//input[@type='submit']")
    button.click()

    button_event_details = selenium.find_element(by=By.XPATH, value="//a[@href='/event_details/1']")
    button_event_details.click()

    sub_title = selenium.find_element(by=By.ID, value="sub-title")
    assert sub_title.is_displayed()


