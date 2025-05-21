import csv
import json
import time
# from xml.etree.ElementTree import indent

import pandas as pd 
from selenium import webdriver  # Import webdriver from selenium-wire
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# from time import sleep
PRESENT_URL = "https://www.oms.enigmatix.co/static/media/tick.09c9652c75f1fd921ec8753c4efc25ce.svg"
ABSENT_URL = "https://www.oms.enigmatix.co/static/media/cross.d66627387f20d569bf425356fad014b6.svg"
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

driver.get ("https://www.oms.enigmatix.co/login")

my_email = driver.find_element(By.CLASS_NAME, 'ant-input')
my_email.send_keys("cs.programmer1115@gmail.com")

login_password = driver.find_element(By.XPATH, "//input[@type='password' and @data-testid='password']")
login_password.send_keys('Lovebirds1433@')

btn_login = driver.find_element(By.XPATH, "//button[@title='LOGIN']")
btn_login.click()

# menue_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ant-avatar') and contains(@class, 'ant-avatar-circle')]")))
# menue_dropdown.click()
menue_dropdown = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='nav-item menu-item-dropdown']")))
menue_dropdown.click()

attendance_page = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/app/employees/attendance']")))
attendance_page.click()

time.sleep(5)  # Wait for the page to load completely
table_trs = driver.find_element(By.TAG_NAME, "table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

MAX_PAGES = 3
current_page = 1

table = driver.find_element(By.TAG_NAME, "table")
# headers = ["Name"]
# headers.extend([th.text for th in table.find_elements(By.XPATH, ".//thead//th")])
headers = [th.text for th in table.find_elements(By.XPATH, ".//thead//th")]

with open("output.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

while current_page <= MAX_PAGES:
    print(f"Scraping Page {current_page}...")
    time.sleep(3)

    for single_tr in table_trs[1:]:
        # print("..text..", single_tr.text)
        tds = single_tr.find_elements(By.TAG_NAME, 'td')
        name = single_tr.text
        present_absent_list = [name]
        for td in tds:
            try:
                attendance_status = td.find_element(By.TAG_NAME, "div").find_element(By.XPATH, "img").get_attribute('src')
            except:
                continue

            if attendance_status == PRESENT_URL:
                print("Present")
                present_absent_list.append("Present")
            elif attendance_status == ABSENT_URL:
                print("Absent")
                present_absent_list.append("Absent")

            else:
                present_absent_list.append("Weekend/OFF")

        with open("output.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(present_absent_list)
    try:
        next_button = driver.find_element(By.XPATH, ".//button//span[@class = 'anticon anticon-right']")
        next_button.click()
        current_page += 1
        time.sleep(2) # Wait for next page to load
    except NoSuchElementException:
        print("Next button not found or last page reached.")
        break

print("✅ CSV file generated successfully.")
driver.quit()
