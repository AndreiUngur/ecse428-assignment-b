import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Get the variables the user must set for the test to run.
# Warn the user if these are not set as the test can not run.
username = os.environ.get("email_username", "")
password = os.environ.get("email_password", "")
recipient = os.environ.get("email_recipient", "")
if not username or not password or not recipient:
    logging.error("Make sure your environment variables are set! "
                  "You must have 'email_username', 'email_password' and 'email_recipient' "
                  "set in your environment.")
    exit()

file_to_send = os.path.join(os.getcwd(), "friendlybug.gif")
if not os.path.exists(file_to_send):
    logging.error("Please ensure the file 'friendlybug.gif' exists in your current directory.")
    exit()

browser = webdriver.Chrome()
browser.get('https://outlook.office.com/mail/inbox')

email_element = browser.find_element_by_name('loginfmt')
email_element.send_keys(username)

continue_button = browser.find_element_by_id('idSIButton9')
continue_button.click()
time.sleep(5)

password_element = browser.find_element_by_id('passwordInput')
password_element.send_keys(password)

login_button = browser.find_element_by_id('submitButton')
login_button.click()
time.sleep(1)

dont_save_login_button = browser.find_element_by_id('idBtn_Back')
dont_save_login_button.click()
time.sleep(1)

new_mail_button = browser.find_element_by_class_name('_39t1Yy85WX6tG-kM3-jR-t')
new_mail_button.click()
time.sleep(1)

recipient_element = browser.find_element_by_class_name('pickerInput_269bfa71')
recipient_element.send_keys(recipient)
time.sleep(0.5)
suggestion_button = browser.find_element_by_id('sug-0')
suggestion_button.click()

subject_element = browser.find_element_by_id('subjectLine0')
subject_element.send_keys("Hello from Selenium!")

attach_button = browser.find_element_by_name('Attach')
browse_button = browser.find_element_by_name('Browse this computer')

attach_button.click()
time.sleep(1)
browse_button.click()
time.sleep(1)
