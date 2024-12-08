from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from llm_chat import radio_query,chat_query
import time
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
load_dotenv()
import os
from selenium.webdriver.common.by import By
# driver=webdriver.Chrome()

# naukri_email=os.getenv("NAUKRI_EMAIL")
# naukri_pass=os.getenv("NAUKRI_PASSWORD")

# driver.get('https://www.naukri.com/nlogin/login')


# wait = WebDriverWait(driver, 5)
# username = driver.find_element("id", "usernameField")
# username.send_keys(naukri_email)
# password=driver.find_element("id", "passwordField")
# password.send_keys(naukri_pass)
# driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(2)
status = True
maxcount=500


applied = 0  # Count of jobs applied sucessfully
failed = 0
max_tries=10

job_link=['/job-listings-ai-ml-engineer-maruti-suzuki-india-limited-gurugram-2-to-6-years-040724502680']
def apply_job (driver):
    chat_history=[]
    tries=0
    status = True
    try:
        already_applied_elements = driver.find_elements(By.ID, "already-applied")
        # alert_elements = driver.find_elements(By.XPATH,
        #                                       "//div[contains(@class, 'styles_alert-message-text') and contains(text(), 'expired')]")
        # print(alert_elements)
        if already_applied_elements:
            print("this is aready applied")
            return False,chat_history


        alert_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'styles_alert-message-text__')]")

        if alert_elements:
            return True,chat_history

        company_site_buttons = driver.find_elements(By.ID, "company-site-button")
        jd_container_elements = driver.find_elements(By.CLASS_NAME, "jdContainer")

        if company_site_buttons:
            print("Apply on company site")
            return False,chat_history
        elif driver.find_elements(By.CLASS_NAME, "jdContainer"):
            return False,chat_history

    except:
        alert_message = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'styles_alert-message-text')]"))
        )
        if alert_message.text:
            return False,chat_history

    if applied <= maxcount:
        try:
            if already_applied_elements:
                return False,chat_history
            driver.find_element(By.XPATH, "//*[text()='Apply']").click()
            # time.sleep(3)

            success_message = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH,"//span[contains(@class, 'apply-message') and contains(text(), 'successfully applied')]")))
            print("Successfully applied.")
            time.sleep(3)
            if success_message:
                return True,chat_history

        except Exception as e:
            print(f"Error during initial apply attempt: {e}")
        while status and tries < max_tries:
            tries=tries+1
            try:
                list_items=WebDriverWait(driver,3).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ssc__listLi"))
                )
                questions = driver.find_elements(By.XPATH, "//li[contains(@class, 'botItem')]/div/div/span")
                for q in questions:
                    question=q.text+"/n"
                print(question)
                options = []
                for index, button in enumerate(list_items, start=1):
                    label = button.find_element(By.CSS_SELECTOR, ".ssc__heading")
                    options.append(f"{index}. {label.text} ")
                    print(options[-1])

                options_str = "\n".join(options)
                user_input_message = f"{question}\n{options_str}"

                selected_option = int(radio_query(user_input_message))
                print(selected_option)
                chat_history.append((question,selected_option))


                selected_button = list_items[selected_option - 1].find_element(By.CSS_SELECTOR, ".ssc__heading")
                print(selected_button)
                driver.execute_script("arguments[0].click();", selected_button)

                # selected_button.click()
                save_button= WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sendMsg")))

                # save_button = WebDriverWait.until(
                #     EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[1]/div[3]/div/div")))
                save_button.click()

                success_message = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//span[contains(@class, 'apply-message') and contains(text(), 'successfully applied')]")))
                if success_message:
                    status = False
            except Exception as e:
                print(f"Error in Search list {e}")
                try:

                    radio_buttons = WebDriverWait(driver, 3).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ssrc__radio-btn-container"))
                    )


                    questions = driver.find_elements(By.XPATH, "//li[contains(@class, 'botItem')]/div/div/span")
                    for q in questions:
                        question=q.text+"/n"
                    print(question)

                    options = []
                    for index, button in enumerate(radio_buttons, start=1):
                        label = button.find_element(By.CSS_SELECTOR, "label")
                        value = button.find_element(By.CSS_SELECTOR, "input").get_attribute("value")
                        options.append(f"{index}. {label.text} (Value: {value})")
                        print(options[-1])

                    options_str = "\n".join(options)
                    user_input_message = f"{question}\n{options_str}"

                    selected_option = int(radio_query(user_input_message))
                    print(selected_option)
                    chat_history.append((user_input_message,selected_option))


                    selected_button = radio_buttons[selected_option - 1].find_element(By.CSS_SELECTOR, "input")
                    print(selected_button)
                    driver.execute_script("arguments[0].click();", selected_button)

                    # selected_button.click()
                    save_button= WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sendMsg")))
                    
                    # save_button = WebDriverWait.until(
                        # EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[1]/div[3]/div/div")))
                    save_button.click()

                    success_message = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//span[contains(@class, 'apply-message') and contains(text(), 'successfully applied')]")))
                    if success_message:
                        status = False

                except Exception as e:
                    print(f"Error during radio button selection or saving: {e}")
                    try:

                        chat_list = WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located((By.XPATH, "//ul[contains(@id, 'chatList_')]"))
                        )


                        li_elements = chat_list.find_elements(By.TAG_NAME, "li")

                        last_question_text = None

                        if li_elements:
                            last_li_element = li_elements[-1]
                            last_question_text = last_li_element.text
                            print("Last question text:", last_question_text)
                        else:
                            print("No <li> elements found.")


                        # question_element = driver.find_element(By.XPATH, "//li[@class='botItem chatbot_ListItem']//div[@class='botMsg msg']//")
                        # question_text = questio   n_element.text
                        # print("Question:", question_text)

                        response = chat_query(last_question_text)
                        print(response)
                        chat_history.append((last_question_text,response))
                        input_field = driver.find_element(By.XPATH, "//div[@class='textArea']")


                        if last_question_text == "Date of Birth":

                            dob = WebDriverWait(driver, 3).until(
                                EC.presence_of_element_located((By.XPATH, "//ul[contains(@id, 'dob__input-container')]"))
                            )
                            dob.send_keys("16022002")

                        if response:
                            input_field.send_keys(response)
                        else:
                            input_field.send_keys("None")
                            print("No response from bard_flash_response.")
                        time.sleep(1)


                        # save_button = input_field.find_element(By.XPATH, "./following-sibling::button[text()='Save']")
                        # save_button = WebDriverWait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[1]/div[3]/div/div")))
                        save_button= WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".sendMsg")))


                        save_button.click()


                        # wait.until(EC.staleness_of(question_element))

                        apply_status_header = driver.find_elements(By.XPATH,"//div[contains(@class, 'apply-status-header') and contains(@class, 'green')]")

                        success_message = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            "//span[contains(@class, 'apply-message') and contains(text(), 'successfully applied')]")))
                        if success_message:
                            status = False

                        if apply_status_header:
                            print("The element exists.")

                        else:
                            print("The element does not exist.")
                    except Exception as e:
                        if already_applied_elements:
                            status = False
                        elif driver.find_elements(By.XPATH,"//div[contains(@class, 'apply-status-header') and contains(@class, 'green')]"):
                            return True,chat_history
                        print(f"Error during fallback procedure: {e}")
                    finally:

                        success_message_elements = driver.find_elements(By.XPATH,
                                                                        "//span[contains(@class, 'apply-message') and contains(text(), 'You have successfully applied')]")

                        if success_message_elements:
                            status = False
    if status:
        return True,chat_history

    return False,chat_history