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

# options = Options()
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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

# Setup Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

user_data_dir = tempfile.mkdtemp()
options.add_argument(f'--user-data-dir={user_data_dir}')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
atexit.register(driver.quit)  # Ensures clean shutdown
driver.maximize_window()

driver.get ("https://www.oms.enigmatix.co/login")

my_email = driver.find_element(By.CLASS_NAME, 'ant-input')
my_email.send_keys("kamran.anwar86@gmail.com")

login_password = driver.find_element(By.XPATH, "//input[@type='password' and @data-testid='password']")
login_password.send_keys('Admin@123')

btn_login = driver.find_element(By.XPATH, "//button[@title='LOGIN']")
btn_login.click()

# menue_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ant-avatar') and contains(@class, 'ant-avatar-circle')]")))
# menue_dropdown.click()
menue_dropdown = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='nav-item menu-item-dropdown']")))
menue_dropdown.click()

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
            json_data = json.loads(response_body)
            
            return json_data

                # Access the 'user' object from the JSON data
            
                
login_response = get_request('api/v1/employee/?login=true')

# Get employee data after login
for key in login_response:
    if key == "user":
    
        user = login_response.get(key)
        print("Employee details:")
        print("First name:", user['first_name'])
        print("Last name:", user['last_name'])
        print("Full name:", user['full_name'])
        print("User email:", user['email'])
        
    if key == "employee_id":
        employee_id = login_response.get(key)
        print("Employee ID:", employee_id)

    if key == 'designation':
        title = login_response.get(key)
        print("Designation:", title['title'])

    if key == "is_active":
        employee_status = login_response.get(key)
        print("Status Active:", employee_status)

    if key == 'availability':
        emp_availability = login_response.get(key)
        print("Availability:", emp_availability)
    
        for role in user['roles']:
           print("Employee role:", role['title'])
        #    print("Role ID:", role['id'])








