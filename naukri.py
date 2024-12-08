from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
load_dotenv()
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from gemini_api import bard_flash_response
import time
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from job_applier import apply_job

import csv
import os

def add_to_csv(job_link, status, chat_history):
    # Path to the CSV file
    file_path = "jobs.csv"
    
    # Check if the file exists; if not, create it and write the header
    file_exists = os.path.isfile(file_path)
    
    # Read the existing job links from the CSV if it exists
    existing_links = set()
    if file_exists:
        with open(file_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            existing_links = {row[0] for row in reader}  # Assuming job_link is the first column

    # Check if the job_link already exists in the CSV
    if job_link in existing_links:
        print(f"The job link '{job_link}' is already present in the CSV.")
    else:
        # Add the new job_link if it doesn't exist
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            # Write the header if the file was just created
            if not file_exists:
                writer.writerow(["Job Link", "Status", "Chat History"])
            
            writer.writerow([job_link, status, chat_history])
        print("Added the job details to the CSV.")


def process_job_tuples(driver,original_window):
    suceess,failure=0,0
    print("in process job tuples")
    # Find all the job tuples by the class name
    scroll_page_down(driver,scroll_duration=5)
    time.sleep(5)
    job_tuples = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")
    
    # Iterate over each job tuple
    for job in job_tuples:
        # Find the link inside the job tuple (anchor tag <a>)
        job_link = job.find_element(By.TAG_NAME, "a")
        
        # Extract the URL from the 'href' attribute of the <a> tag
        job_url = job_link.get_attribute("href")
        
        # Open the link in a new tab
        driver.execute_script(f"window.open('{job_url}', '_blank');")
    
        
        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(5)
        
        # Call the function to scrape the new tab
        is_success,chat_history=scrape_new_tab(driver)
        if is_success:
            print("Successfully Applied!")
            add_to_csv(job_url,is_success,chat_history)
            suceess=suceess+1
        else:
            print("Failure , adding data to csv")
            add_to_csv(job_url,is_success,chat_history)
            failure=failure+1
        
        # Close the new tab after scraping
        driver.close()
        
        # Switch back to the original tab (main window)
        driver.switch_to.window(original_window)
        
        # Optionally, wait for a moment before continuing with the next job tuple
        time.sleep(2)
    return suceess,failure


def scrape_new_tab(driver):
    # Wait for the new tab to load (you can adjust the waiting strategy as per the page load)
    time.sleep(3)
    
    # Perform your scraping tasks here
    # For example, print the page title
    print(f"Scraping page: {driver.title}")
    
    # Scrape specific data, like the job description, etc.
    # For example:
    is_success,chat_history =apply_job(driver)
    return is_success,chat_history
    
def scroll_page_down(driver,scroll_duration):
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    # Set the number of steps for scrolling
    steps = 50  # Increase for smoother scrolling

    # Calculate the delay between each step
    step_delay = scroll_duration / steps

    # Calculate the amount to scroll in each step
    scroll_increment = scroll_height / steps

    # Perform the scroll in increments
    for step in range(steps):
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(step_delay)  # Delay between each scroll increment

import time

def scroll_page_up(driver, scroll_duration):
    # Get the current scroll position (from the bottom)
    scroll_height = driver.execute_script("return document.body.scrollHeight")

    # Set the number of steps for scrolling
    steps = 50  # Increase for smoother scrolling

    # Calculate the delay between each step
    step_delay = scroll_duration / steps

    # Calculate the amount to scroll in each step
    scroll_increment = scroll_height / steps

    # Perform the scroll in increments (scrolling up requires a negative value)
    for step in range(steps):
        driver.execute_script(f"window.scrollBy(0, -{scroll_increment});")
        time.sleep(step_delay)  # Delay between each scroll increment


### load selenium driver
driver = webdriver.Chrome()
driver.maximize_window()
sleep(1)
naukri_email=os.getenv("NAUKRI_EMAIL")
naukri_pass=os.getenv("NAUKRI_PASSWORD")

driver.get('https://www.naukri.com/nlogin/login')


wait = WebDriverWait(driver, 5)
username = driver.find_element("id", "usernameField")
username.send_keys(naukri_email)
password=driver.find_element("id", "passwordField")
password.send_keys(naukri_pass)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(2)
driver.get("https://www.naukri.com/ai-ml-engineer-ml-engineer-natural-language-processing-artificial-intelligence-jobs-in-remote?k=ai%20ml%20engineer%2C%20ml%20engineer%2C%20natural%20language%20processing%2C%20artificial%20intelligence&l=remote%2C%20delhi%20%2F%20ncr%2C%20gurugram%2C%20noida&nignbevent_src=jobsearchDeskGNB&experience=1&functionAreaIdGid=3")
# driver.get("https://www.naukri.com/ai-ml-engineer-ml-engineer-natural-language-processing-artificial-intelligence-jobs-in-remote?k=ai%20ml%20engineer%2C%20ml%20engineer%2C%20natural%20language%20processing%2C%20artificial%20intelligence&l=remote%2C%20delhi%20%2F%20ncr%2C%20gurugram%2C%20noida&nignbevent_src=jobsearchDeskGNB&experience=1&wfhType=0&wfhType=2")
original_window=driver.current_window_handle
time.sleep(10)
# process_job_tuples(driver,original_window)
applied=0
max_apply=150
while(applied<max_apply):
    job_tuples = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")
    print(job_tuples)
    success_apply,failed_apply=process_job_tuples(driver,original_window)
    applied=applied+success_apply
    # goto next page
    time.sleep(5) 
    scroll_page_up(driver,5)
    next_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="lastCompMark"]//a[.//span[text()="Next"]]'))
)
    next_button.click()
    # next_buttons=driver.find_elements(By.CLASS_NAME,".styles_btn-secondary__2AsIP")
    # for button in next_buttons:
    #     span_element = button.find_element(By.TAG_NAME, "span")
        
    #     # Access the text of the span element
    #     span_text = span_element.text
    #     if span_text=="Next":
    #         driver.execute_script("arguments[0].click();", button)
    #         break

    time.sleep(5)
driver.quit()
