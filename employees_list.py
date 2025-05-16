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

# Get response from the api/header
def get_request(endpoint):
    for request in driver.requests:
        if request.response:
            if endpoint in request.url:
                print(f"URL: {request.url}")
                print(f"Status Code: {request.response.status_code}")
                response_body = request.response.body.decode('utf-8')
                json_data = json.loads(response_body)
                # print("Response Body (JSON):", json.dumps(json_data, indent=4))  # Pretty print the JSON data
                return json_data
                


options = Options()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

driver.get("https://www.oms.enigmatix.co/login")

my_email = driver.find_element(By.CLASS_NAME, 'ant-input')
my_email.send_keys("kamran.anwar86@gmail.com")

login_password = driver.find_element(By.XPATH, "//input[@type='password' and @data-testid='password']")
login_password.send_keys('Admin@123')

btn_login = driver.find_element(By.XPATH, "//button[@title='LOGIN']")
btn_login.click()

emp_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/app/employee/employees"]')))
emp_tab.click()

time.sleep(5)


employees = get_request('api/v1/employee/all_employees_list/')
# print(employees)

# Get Employee details from the employee list

for emp in employees:
    name = emp.get('full_name')
    if name == "Muhammad Kamran Anwar":
        print("name:",name)
        status = emp.get('status')
        print("EMP status:",status)
        employee_id = emp.get("employee_id")
        print("Employee ID:", employee_id)


driver.quit()