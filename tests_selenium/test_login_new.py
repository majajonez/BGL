from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from tests_selenium.fake_data import Random_user

selenium = webdriver.Chrome()

user = Random_user()

def test_login():
    selenium.get('http://127.0.0.1:5000/auth/login')

    login_input = selenium.find_element(by=By.ID, value='username')
    password_input = selenium.find_element(by=By.ID, value='password')

    login_input.send_keys('maja')
    password_input.send_keys('123')

    button = selenium.find_element(by=By.XPATH, value="//input[@type='submit']")
    button.click()

    logout_btn = selenium.find_element(by=By.ID, value="logout_button")
    assert logout_btn.is_displayed()


def test_register():
    selenium.get('http://127.0.0.1:5000/auth/register')

    login_input = selenium.find_element(by=By.ID, value='username')
    password_input = selenium.find_element(by=By.ID, value='password')
    email_input = selenium.find_element(by=By.ID, value='email')
    city_input = selenium.find_element(by=By.ID, value='city')

    login_input.send_keys(user.name)
    password_input.send_keys(user.password)
    email_input.send_keys(user.email)
    city_input.send_keys(user.city)

    button = selenium.find_element(by=By.XPATH, value="//input[@type='submit']")
    button.click()

    login_input_2 = selenium.find_element(by=By.ID, value='username')
    password_input_2 = selenium.find_element(by=By.ID, value='password')

    login_input_2.send_keys(user.name)
    password_input_2.send_keys(user.password)

    button = selenium.find_element(by=By.XPATH, value="//input[@type='submit']")
    button.click()

    logout_btn = selenium.find_element(by=By.ID, value="logout_button")
    assert logout_btn.is_displayed()


def test_logout():
    selenium.get('http://127.0.0.1:5000/auth/login')

    login_input = selenium.find_element(by=By.ID, value='username')
    password_input = selenium.find_element(by=By.ID, value='password')

    login_input.send_keys('maja')
    password_input.send_keys('123')

    button = selenium.find_element(by=By.XPATH, value="//input[@type='submit']")
    button.click()

    logout_btn = selenium.find_element(by=By.ID, value="logout_button")
    logout_btn.click()

    login_btn = selenium.find_element(by=By.ID, value="login_button")

    assert login_btn.is_displayed()

