# from xml.etree.ElementTree import indent
import json
import time
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

courts_list = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/events']")))
courts_list.click()

# courts_campaign = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div[4]/div/div/div[2]/div/div[2]/div/div[1]/div/div[3]/button/span")))
# courts_campaign.click()
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




event_data = get_request("api/v1/events/?type=game&club=199&page=1&sort=")


for key in event_data:
    if key == "results":
        result = event_data.get(key)
        for record in result:
            if record['title'] == "Flamurtari football game":
                print("Title:", record["title"])
                print("Event Type:", record["event_type"])
                print("Court Name:", record["court_detail"]['title'])

