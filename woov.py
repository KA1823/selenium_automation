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
driver.get ("https://dev.woovclub.com/login")

my_email = driver.find_element(By.XPATH, '//input[@type="email" and @id="email"]')
my_email.send_keys("one75449@gmail.com")

login_password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
login_password.send_keys('Pass@123')

login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='whitespace-nowrap flex text-nowrap font-semibold rtl:not-italic italic items-center lineHeight30 py-3 px-5 text-xl  ']")))
login_button.click()

courts_list = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href = '/courts']")))
courts_list.click()

time.sleep(5)

def get_request(endpoint):
    for request in driver.requests:
        if request.response:
            if endpoint in request.url:
                print(f"URL: {request.url}")
                print(f"Status Code: {request.response.status_code}")
                respon_body = request.response.body.decode('utf-8')
                json_data = json.loads(respon_body)
                return json_data




court_data = get_request("api/v1/web-courts/?sports=&sort=")


for key in court_data:
    title = key.get("title")
    if title == "New paintball court":
        print("Court name:", title)
        print("Court ID:", key['id'])
        print("Players Count:", key['number_of_players'])
        print("Club ID:", key['club'])
        print("Average Rating:", key['avg_rating'])
        print("Booking Count:", key['booking_count'])
        future_bookings = key.get("total_future_bookings")
        print("Court Future Bokings:", future_bookings)
