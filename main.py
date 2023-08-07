from selenium import webdriver
from selenium.common import NoSuchElementException
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
contract_type = []
work_schedule = []
experience_level = []
type_of_work = []
required_technologies = []
optional_technologies = []
responsibilities_section = []
requirements_section = []
optional_section = []


for job_offer in links[0:5]:
    driver.get(job_offer)
    time.sleep(5)
    try:
        company_name_element = driver.find_element(By.CSS_SELECTOR,
                                               'h2[data-test="text-employerName"]').text.replace("O firmie", "")
        company_name_element = company_name_element.replace("About the company", "")
    except NoSuchElementException:
        company_name_element = None

    try:
        position_name_element = driver.find_element(By.CSS_SELECTOR,
                                            'h1[data-test="text-positionName"]').text
    except NoSuchElementException:
        position_name_element = None

    try:
        localisation_element = driver.find_element(By.CSS_SELECTOR,
                                                'div[data-test="sections-benefit-workplaces"]').text.replace("Siedziba firmy", "")
        localisation_element = localisation_element.replace("Company location", "")
    except NoSuchElementException:
        localisation_element = None

    try:
        contract_type_element = driver.find_element(By.CSS_SELECTOR,
                                                'div[data-test="sections-benefit-contracts-text"]').text
    except NoSuchElementException:
        contract_type_element = None

    try:
        work_schedule_element = driver.find_element(By.CSS_SELECTOR,
                                                'div[data-test="sections-benefit-work-schedule-text"]').text
    except NoSuchElementException:
        work_schedule_element = None

    try:
        experience_level_element = driver.find_element(By.CSS_SELECTOR,
                                                   'div[data-test="sections-benefit-employment-type-name-text"]').text
    except NoSuchElementException:
        experience_level_element = None

    try:
        type_of_work_element = driver.find_element(By.CSS_SELECTOR,
                                                'div[data-test="sections-benefit-work-modes-text"]').text
    except NoSuchElementException:
        type_of_work_element = None

    try:
        required_technologies_element = driver.find_element(By.CSS_SELECTOR,
                                               'div[data-test="section-technologies-expected"]').text.replace("Wymagane", "")
        required_technologies_element = required_technologies_element.replace("Expected","")
    except NoSuchElementException:
        required_technologies_element = None

    try:
        optional_technologies_element = driver.find_element(By.CSS_SELECTOR,
                                                        'div[data-test="section-technologies-optional"]').text.replace("Mile widziane", "")
        optional_technologies_element = optional_technologies_element.replace("Optional", "")
    except NoSuchElementException:
        optional_technologies_element = None

    try:
        responsibilities_section_element = driver.find_element(By.CSS_SELECTOR,
                                               'div[data-test="section-responsibilities"]').text.replace("Twój zakres obowiązków", "")
        responsibilities_section_element = responsibilities_section_element.replace("Your responsibilities", "")
    except NoSuchElementException:
        responsibilities_section_element = None

    try:
        requirements_section_element = driver.find_element(By.CSS_SELECTOR,
                                                   'div[data-test="section-requirements-expected"]').text
    except NoSuchElementException:
        requirements_section_element = None

    try:
        optional_section_element = driver.find_element(By.CSS_SELECTOR,
                                                   'div[data-test="section-requirements-optional"]').text.replace("Mile widziane", "")
        optional_section_element = optional_section_element.replace("Optional", "")
    except NoSuchElementException:
        optional_section_element = None

    company_name.append(company_name_element)
    position_name.append(position_name_element)
    link_to_offer.append(job_offer)
    localisation.append(localisation_element)
    contract_type.append(contract_type_element)
    work_schedule.append(work_schedule_element)
    experience_level.append(experience_level_element)
    type_of_work.append(type_of_work_element)
    required_technologies.append(required_technologies_element)
    optional_technologies.append(optional_technologies_element)
    responsibilities_section.append(responsibilities_section_element)
    requirements_section.append(requirements_section_element)
    optional_section.append(optional_section_element)


data = pd.DataFrame(
    {
        "company_name": company_name,
        "position_name": position_name,
        "link_to_offer": link_to_offer,
        "localisation": localisation,
        "contract_type": contract_type,
        "work_schedule": work_schedule,
        "experience_level": experience_level,
        "type_of_work": type_of_work,
        "required_technologies": required_technologies,
        "optional_technologies": optional_technologies,
        "responsibilities_section": responsibilities_section,
        "requirements_section": requirements_section,
        "optional_section": optional_section
                     })
data.to_csv("job_offers.csv", index=False)

offers = pd.read_csv("job_offers.csv")
print(offers)

driver.quit()

