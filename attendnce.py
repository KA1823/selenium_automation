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
driver.get("https://www.oms.enigmatix.co/login")

# Login
driver.find_element(By.CLASS_NAME, 'ant-input').send_keys("kamran.anwar86@gmail.com")
driver.find_element(By.XPATH, "//input[@type='password' and @data-testid='password']").send_keys('Admin@123')
driver.find_element(By.XPATH, "//button[@title='LOGIN']").click()

# Navigate to Attendance
menue_dropdown = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='nav-item menu-item-dropdown']")))
menue_dropdown.click()

attendance_page = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/app/employees/attendance']")))
attendance_page.click()

time.sleep(5)  # Give time for network requests to fire

# API Interception
def get_request(endpoint):
    for request in driver.requests:
        if request.response and endpoint in request.url:
            print(f"URL: {request.url}")
            print(f"Status Code: {request.response.status_code}")
            response_body = request.response.body.decode('utf-8')
            return json.loads(response_body)
    return None

attendance = get_request('api/v1/attendance/todays_timesheet')
if not attendance:
    print("❌ No attendance data captured from API.")
else:
    print("Attendance Status:", attendance.get("status"))
    print("First Check in:", attendance.get("first_check_in"))
    print("Last Check in:", attendance.get("last_check_in"))
