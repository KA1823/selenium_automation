import chromedriver_autoinstaller
from selenium import webdriver

# Automatically install and configure ChromeDriver
chromedriver_autoinstaller.install()  # This will download and install the matching ChromeDriver

# Create a new instance of Chrome WebDriver
driver = webdriver.Chrome()

# Open Google
driver.get("https://www.tripadvisor.co.uk/")

# Print the page title
print(f"Page title is: {driver.title}")

# Optionally, close the browser after some time
# driver.quit()