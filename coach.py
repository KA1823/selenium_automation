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

coach_list = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/coaches']")))
coach_list.click()

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




coach_data = get_request("api/v1/coach/?page=1")

for key in coach_data:
    if key == 'results':
        result = coach_data.get(key)
        # print("Results:", result)

        for coach in result:
            if coach['id'] == 30:
                print("Coach One:")
                print("Coach Name:", coach['name'])
                print("Rating:", coach['avg_rating'])
                print("Experience:", coach['experience'])
            
            # if coach['id'] == 36:
            #     print("Coach Two:")
            #     print("Coach Name:", coach['name'])
            #     print("Rating:", coach['avg_rating'])
            #     print("Experience:", coach['experience'])




coach_list = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/posts']")))
coach_list.click()

time.sleep(5)

def get_post(post):
    for request in driver.requests:
        if request.response:
            if post in request.url:
                print("Post Data:")
                print(f"URL: {request.url}")
                print(f"Status Code: {request.response.status_code}")
                response = request.response.body.decode('utf-8')
                json_load = json.loads(response)
                return json_load
            

post_data = get_post('api/v1/get-web-post/?page=1&filter=128')


for user_post in post_data:
    if user_post == 'results':
        club_post = post_data.get(user_post)
        # print("Post Data:", club_post)
        for current_post in club_post:
            if current_post['id'] == 387:
                print("Post Title:", current_post['title'])
                print("Created at:", current_post['created_at'])
                print("Post Views:", current_post['views'])
                print("Visibility:", current_post['visibility'])