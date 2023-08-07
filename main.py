from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

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

company_name = []
position_name = []
link_to_offer = []
localisation = []
contact_type = []
experience_level = []
type_of_work = []
requirements = []
good_to_have = []



for job_offer in offer_to_scrape:
    driver.get(job_offer)
    employer_name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                       'h2[data-test="text-employerName"]')))
    employer = employer_name_element.text.replace("O firmie", "")
    position_name_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                       'h1[data-test="text-positionName"]')))

    position = position_name_element.text
    print(employer)
    print(position)







data = pd.DataFrame({"company_name": company_name,
                     "position_name": position_name,
                     "link_to_offer": link_to_offer,
                     "localisation": localisation,
                     "contact_type": contact_type,
                     "experience_level": experience_level,
                     "type_of_work": type_of_work,
                     "requirements": requirements,
                     "good_to_have": good_to_have
                     })
data.to_csv("job_offers.csv")

offers = pd.read_csv("job_offers.csv")
print(offers)

time.sleep(300)
driver.quit()

