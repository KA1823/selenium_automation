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

courts_list = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href = '/campaigns']")))
courts_list.click()

courts_campaign = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div[4]/div/div/div[2]/div/div[2]/div/div[1]/div/div[3]/button/span")))
courts_campaign.click()
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




court_data = get_request("api/v1/campaigns/?page=1&type=court")


for key in court_data:
    if key == 'results':
        results = court_data.get(key)
        # print("Results:", results)
        for data in results:
            if data['uuid'] == "1ae10d62-b98b-4f8a-9c86-e8caeb011b3e":
                print("First Campaign:")
                print("Campaign Title:",data['campaign_title'])

                for sports in data["sports_detail"]:
                    if sports['id'] == 2:
                        print("Sports name:", sports['name'])

            
            if data['uuid'] == "17f4074d-92b4-4604-b1af-e77bf98b20d3":
                print("Second Campaign:")
                print("Campaign Title two:", data['campaign_title'])
                print ("Sports name:", sports['name'])








a = ['https://www.tripadvisor.co.uk/AttractionProductReview-g189180-d11455798-Douro_Valley_..._Lunch_Cruise-Porto_Porto_District_No.html', 'https://www.tripadvisor.co.uk/AttractionProductReview-g189180-d16796856-Douro_Valley_...ise_Winery_Lunch-Porto_Porto_District.html', 'https://www.tripadvisor.co.uk/AttractionProductReview-g189180-d11472212-Authentic_Dou..._River_Cruise-Porto_Porto_District_No.html', 'https://www.tripadvisor.co.uk/AttractionProductReview-g189180-d13351949-Douro_Valley_...tional_Boat_Cruise-Porto_Porto_Distri.html', 'https://www.tripadvisor.co.uk/AttractionProductReview-g189180-d11485347-Douro_Valley_...ch_from_Porto-Porto_Porto_District_No.html', 'https://www.tripadvisor.co.uk/AttractionProductReview-g189180-d11475126-Douro_Valley_...unch_Tastings-Porto_Porto_District_No.html', 'https://www.tripadvisor.co.uk/AttractionProductReview-g189180-d11475603-Douro_Valley_...ng_Lunch_and_Boat-Porto_Porto_Distric.html', 'https://www.tripadvisor.co.uk/AttractionProductReview-g189180-d25419774-Premium_Smal...
