from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)
wait_long = WebDriverWait(driver, 10)

driver.get("https://www.pracuj.pl/")

search_phrase = "Python"

driver.maximize_window()

cookie_agreement = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="button-submitCookie"]')))
cookie_agreement.click()

search_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test="input-field"]')))
search_field.send_keys(search_phrase)

search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Szukaj")]')))
search_button.click()

multiple_localisation = wait_long.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-test-location="multiple"]')))

for offer_with_multiple_localisation in multiple_localisation:
    offer_with_multiple_localisation.click()

offers_current_page = wait_long.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@data-test="link-offer"]')))
links = [offer.get_attribute("href") for offer in offers_current_page]
print(links)


offer_to_scrape = ["https://www.pracuj.pl/praca/programista-w-dziale-rnd-wroclaw-kazimierza-witalisa-szarskiego-3,oferta,1002772799?s=499ee8a1&searchId=MTY5MTQxNDAwMjU4NC42MDg2"]

for job_offer in offer_to_scrape:
    driver.get(job_offer)

time.sleep(300)
driver.quit()

