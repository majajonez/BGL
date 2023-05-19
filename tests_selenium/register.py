from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from tests_selenium.fake_data import Random_user

path = 'C:\\Users\\kasper\\PycharmProjects\BGL\\tests_selenium\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=path)

driver.get('http://127.0.0.1:5000/auth/register')

sleep(2)

login_input = driver.find_element(by=By.ID, value='username')
password_input = driver.find_element(by=By.ID, value='password')
email_input = driver.find_element(by=By.ID, value='email')
city_input = driver.find_element(by=By.ID, value='city')

user = Random_user()

login_input.send_keys(user.name)
password_input.send_keys(user.password)
email_input.send_keys(user.email)
city_input.send_keys(user.city)

button = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
button.click()

login_input_2 = driver.find_element(by=By.ID, value='username')
password_input_2 = driver.find_element(by=By.ID, value='password')

login_input_2.send_keys(user.name)
password_input_2.send_keys(user.password)

button = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
button.click()

sleep(5)

driver.close()
