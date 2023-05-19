from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

path = 'C:\\Users\\kasper\\PycharmProjects\BGL\\tests_selenium\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=path)

driver.get('http://127.0.0.1:5000/auth/register')

sleep(2)

login_input = driver.find_element(by=By.ID, value='username')
password_input = driver.find_element(by=By.ID, value='password')
email_input = driver.find_element(by=By.ID, value='email')
city_input = driver.find_element(by=By.ID, value='city')

login_input.send_keys('kasper')
password_input.send_keys('qwe')
email_input.send_keys('kasper@gmail.com')
city_input.send_keys('warszawa')

button = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
button.click()

login_input_2 = driver.find_element(by=By.ID, value='username')
password_input_2 = driver.find_element(by=By.ID, value='password')

login_input_2.send_keys('maja')
password_input_2.send_keys('123')

button = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
button.click()

sleep(5)

driver.close()
