import json
import time
import tempfile
import atexit

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Helper function to fetch API data ---
def get_request(endpoint):
    for request in driver.requests:
        if request.response and endpoint in request.url:
            print(f"📡 Intercepted URL: {request.url}")
            print(f"✅ Status Code: {request.response.status_code}")
            response_body = request.response.body.decode('utf-8')
            return json.loads(response_body)
    return None

# --- Setup Chrome WebDriver for Jenkins/CI ---
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')  # Required for some CI environments
options.add_argument('--disable-dev-shm-usage')  # Prevents shared memory issues

# Create a unique temporary user data dir to avoid session conflicts
user_data_dir = tempfile.mkdtemp()
options.add_argument(f'--user-data-dir={user_data_dir}')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
atexit.register(driver.quit)  # Ensures driver quits on exit
driver.maximize_window()

# --- Login Sequence ---
driver.get("https://www.oms.enigmatix.co/login")

driver.find_element(By.CLASS_NAME, 'ant-input').send_keys("kamran.anwar86@gmail.com")
driver.find_element(By.XPATH, "//input[@type='password' and @data-testid='password']").send_keys('Admin@123')
driver.find_element(By.XPATH, "//button[@title='LOGIN']").click()

# --- Navigate to Employee Tab ---
emp_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/app/employee/employees"]')))
emp_tab.click()
time.sleep(5)  # Let API calls load

# --- Fetch API data ---
employees = get_request('api/v1/employee/all_employees_list/')
if not employees:
    print("❌ Employee data not found.")
    exit(1)

# --- Parse Employee Info ---
for emp in employees:
    name = emp.get('full_name')
    if name == "Muhammad Kamran Anwar":
        print("✅ Name:", name)
        print("   Status:", emp.get('status'))
        print("   Employee ID:", emp.get("employee_id"))

# import json
# import time
# # from xml.etree.ElementTree import indent

# from seleniumwire import webdriver  # Import webdriver from selenium-wire
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# # from time import sleep

# # Get response from the api/header
# def get_request(endpoint):
#     for request in driver.requests:
#         if request.response:
#             if endpoint in request.url:
#                 print(f"URL: {request.url}")
#                 print(f"Status Code: {request.response.status_code}")
#                 response_body = request.response.body.decode('utf-8')
#                 json_data = json.loads(response_body)
#                 # print("Response Body (JSON):", json.dumps(json_data, indent=4))  # Pretty print the JSON data
#                 return json_data
                


# options = Options()

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.maximize_window()

# driver.get("https://www.oms.enigmatix.co/login")

# my_email = driver.find_element(By.CLASS_NAME, 'ant-input')
# my_email.send_keys("kamran.anwar86@gmail.com")

# login_password = driver.find_element(By.XPATH, "//input[@type='password' and @data-testid='password']")
# login_password.send_keys('Admin@123')

# btn_login = driver.find_element(By.XPATH, "//button[@title='LOGIN']")
# btn_login.click()

# emp_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/app/employee/employees"]')))
# emp_tab.click()

# time.sleep(5)


# employees = get_request('api/v1/employee/all_employees_list/')
# # print(employees)

# # Get Employee details from the employee list

# for emp in employees:
#     name = emp.get('full_name')
#     if name == "Muhammad Kamran Anwar":
#         print("name:",name)
#         status = emp.get('status')
#         print("EMP status:",status)
#         employee_id = emp.get("employee_id")
#         print("Employee ID:", employee_id)


# driver.quit()