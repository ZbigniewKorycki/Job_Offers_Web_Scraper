from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://www.pracuj.pl/")

cookie_agreement = driver.find_element(By.CSS_SELECTOR, '[data-test="button-submitCookie"]')
cookie_agreement.click()

time.sleep(300)
driver.quit()

