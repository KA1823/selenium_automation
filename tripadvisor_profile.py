import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse



class TripAdvisor():

    def __init__(self):
        self.main_tour_links = []
        self.data = {"Tour Name": [], "Contact number": [], "Contact email":[], "Website link": []}
        driver = self.open_browser("https://www.tripadvisor.co.uk/Attractions-g189180-Activities-c42-Porto_Porto_District_Northern_Portugal.html")
        self.get_main_tours_urls(driver)
        self.get_specific_tour_details()

    def close_browser(self, driver):
        driver.quit()

    def open_browser(self, link):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        driver.get(link)
        return driver


    def get_existing_df_and_append(self, result_data):
        output_file = f"{os.getcwd()}/output.csv"
        # try:
        #     existing_df = pd.read_csv(output_file)
        # except FileNotFoundError:
        #     existing_df = pd.DataFrame()
        df = pd.DataFrame(result_data)
        df.to_csv(f'{output_file}')
        # combined_data = pd.concat([existing_df, df], ignore_index=True)
        # combined_data.to_csv(f'{output_file}', index=False)
        return True
    


    def get_all_reviews(self, driver):
        reviews_list = []
        reviews_divs = driver.find_elements(By.XPATH, "//div[@class = '_c' and @data-automation='reviewCard']")
        time.sleep(5)
        for idx, review in enumerate(reviews_divs):
            reviewer_text = review.find_element(By.XPATH, ".//*[contains(@class, 'zpDvc Zb')]").find_element(By.TAG_NAME, 'a').text
            try:
                ratings = review.find_element(By.XPATH, ".//*[contains(@class, 'UctUV d H0')]").find_element(By.TAG_NAME, "title").text
                ratings = ratings.split(' of')[0]
            except:
                ratings = 0
            review_text = review.find_element(By.XPATH, ".//*[contains(@class, '_T FKffI')]").text
            reviews_list.append(f"{reviewer_text}--{ratings}--{review_text}")
        return '\n'.join(reviews_list)
    


    def get_main_tours_urls(self, driver):
        time.sleep(10)
        main_tour_divs = driver.find_elements(By.XPATH, "//*[contains(@class, 'hZuqH y')]")
        for main_tour_div in main_tour_divs[:15]:
            url = main_tour_div.find_elements(By.TAG_NAME, 'a')[0].get_attribute("href")
            self.main_tour_links.append(url)
        self.close_browser(driver)


    def get_tour_planner_details(self, driver):
        contact = "N-A"
        email = "N-A"
        website_link = "N-A"
        try:
            link = driver.find_element(By.XPATH, "//a[@class = 'BMQDV _F Gv wSSLS SwZTJ FGwzt PaRlG']").get_attribute("href")
            driver.get(link)
            # contact_tel = []
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable("//a[@class = 'UikNM _G B- _S _W _T c G_ wSSLS wnNQG raEkE' and @rel='nofollow']"))
            time.sleep(4)
            contact_details =  driver.find_elements(By.XPATH, "//a[@class = 'UikNM _G B- _S _W _T c G_ wSSLS wnNQG raEkE' and @rel='nofollow']")
            # contact_dropdown = driver.find_element(By.XPATH, "//span[@class = 'biGQs _P XWJSj Wb' and @text()='Contact']").click()


            for details in contact_details:
                href_string = details.get_attribute("href")
                if href_string.startswith("tel"):
                    contact = urllib.parse.unquote(href_string)
                    contact = contact.split("tel:")[1]

                if href_string.startswith("mailto"):
                    email = urllib.parse.unquote(href_string)
                    email = email.split("mailto:")[1]


                if href_string.startswith("http"):
                    website_link = urllib.parse.unquote(href_string)
            return contact, email, website_link
        except:
            return contact, email, website_link

    def get_specific_tour_details(self):
        for link in self.main_tour_links:
            try:
                driver = self.open_browser(link)
                time.sleep(5)
                title = driver.find_elements(By.TAG_NAME, "h1")[0].text
                # about = driver.find_element(By.XPATH, "//*[contains(@class, '_d')]").text
                time.sleep(4)
                # price = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'biGQs _P fiohW avBIb uuBRH')]"))).text
                # reviews = self.get_all_reviews(driver)
                self.data['Tour Name'].append(title)
                # self.data['Price'].append(price)
                # self.data['About'].append(about)
                # self.data['Reviews'].append(reviews)

                contact, email, website = self.get_tour_planner_details(driver)
                time.sleep(4)
                self.data["Contact number"].append(contact)
                self.data["Contact email"].append(email)
                self.data["Website link"].append(website)

                self.close_browser(driver)
            except Exception as e:
                continue
        self.get_existing_df_and_append(self.data)


trip = TripAdvisor()