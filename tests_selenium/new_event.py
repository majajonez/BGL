from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

path = 'C:\\Users\\kasper\\PycharmProjects\BGL\\tests_selenium\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=path)

driver.get('http://127.0.0.1:5000/auth/login')

sleep(2)

login_input = driver.find_element(by=By.ID, value='username')
password_input = driver.find_element(by=By.ID, value='password')

login_input.send_keys('maja')
password_input.send_keys('123')

button = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
button.click()

button_confirm_event = driver.find_element(by=By.XPATH, value="//a[@href='/event']")
button_confirm_event.click()

title_input = driver.find_element(by=By.ID, value='title')
description_input = driver.find_element(by=By.ID, value='description')
when_input = driver.find_element(by=By.ID, value='when')
where_input = driver.find_element(by=By.ID, value='where')
seats_input = driver.find_element(by=By.ID, value='the_number_of_seats')

title_input.send_keys('gra testowa')

description_input.send_keys('testy tworzenia wydarzeń')

when_input.send_keys('01.02.2023')

where_input.send_keys('Warszawa')

seats_input.send_keys('4')


button_confirm_event = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
button_confirm_event.click()

sleep(3)

driver.close()
