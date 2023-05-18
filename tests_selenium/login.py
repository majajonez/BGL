from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


path = 'C:\\Users\\kasper\\PycharmProjects\BGL\\tests_selenium\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=path)

# driver.get('https://duckduckgo.com')
#
# duck = driver.find_element_by_id('logo_homepage_link')
#
# duck.click()
# print(duck.get_attribute('outerHTML'))
#
# try:
#     duck = driver.find_element_by_id('logo_homepage_link')
# except NoSuchElementException:
#     print('Nie ma takiego elementu')