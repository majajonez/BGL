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

sleep(2)

driver.close()





# duck.click()
# print(duck.get_attribute('outerHTML'))
#
# try:
#     duck = driver.find_element_by_id('logo_homepage_link')
# except NoSuchElementException:
#     print('Nie ma takiego elementu')