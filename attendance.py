import json
import time
# from xml.etree.ElementTree import indent

from seleniumwire import webdriver  # Import webdriver from selenium-wire
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# from time import sleep

options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

driver.get ("https://www.oms.enigmatix.co/login")

my_email = driver.find_element(By.CLASS_NAME, 'ant-input')
my_email.send_keys("kamran.anwar86@gmail.com")
# print("email", my_email.get_attribute("value"))

login_password = driver.find_element(By.XPATH, "//input[@type='password' and @data-testid='password']")
login_password.send_keys('Admin@123')
# print("password", login_password.get_attribute("value"))
btn_login = driver.find_element(By.XPATH, "//button[@title='LOGIN']")
btn_login.click()

# menue_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ant-avatar') and contains(@class, 'ant-avatar-circle')]")))
# menue_dropdown.click()
menue_dropdown = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='nav-item menu-item-dropdown']")))
menue_dropdown.click()

attendance_page = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/app/employees/attendance']")))
attendance_page.click()

time.sleep(5)

# Get response from the api/header

def get_request(endpoint):
    for request in driver.requests:
        if request.response:
        # Filter the API requests based on the URL or other criteria
         if endpoint in request.url:  # Replace with the API endpoint
            print(f"URL: {request.url}")
            print(f"Status Code: {request.response.status_code}")  
            # Decode the response body from bytes to a string
            response_body = request.response.body.decode('utf-8')
            # print("Body:", response_body)               
            json_data = json.loads(response_body)
            # print("json data:", json_data)
            return json_data

                       
            


attendance = get_request('api/v1/attendance/todays_timesheet')

# get employee attendance record

for emp in attendance:
   if emp == "status":
    status = attendance.get(emp)   
    print("Attendance Status:", status)
    check_in_first = attendance.get('first_check_in')
    print("First Check in", check_in_first)
    check_in_last = attendance.get('last_check_in')
    print("Last Check in", check_in_last)