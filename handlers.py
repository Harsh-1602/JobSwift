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

def process_job_tuples(driver,original_window):
    print("in process job tuples")
    # Find all the job tuples by the class name
    scroll_page(driver,scroll_duration=5)
    driver.close()
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
        scrape_new_tab(driver)
        
        # Close the new tab after scraping
        driver.close()
        
        # Switch back to the original tab (main window)
        driver.switch_to.window(original_window)
        
        # Optionally, wait for a moment before continuing with the next job tuple
        time.sleep(2)


def scrape_new_tab(driver):
    # Wait for the new tab to load (you can adjust the waiting strategy as per the page load)
    time.sleep(3)
    
    # Perform your scraping tasks here
    # For example, print the page title
    print(f"Scraping page: {driver.title}")
    
    # Scrape specific data, like the job description, etc.
    # For example:
    apply_job(driver)
    
def scroll_page(driver,scroll_duration):
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

    # Optional: Wait to observe the scroll completion
    time.sleep(2)
