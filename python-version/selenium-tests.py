import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

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

# Ensure the image we want to send exists.
file_to_send = os.path.join(os.getcwd(), "friendlybug.gif")
if not os.path.exists(file_to_send):
    logging.error("Please ensure the file 'friendlybug.gif' exists in your current directory.")
    exit()
email_subject = "Hello from Selenium!"

# Log in to the sender's account
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

# Verify that no such email exists yet
sent_emails_button = browser.find_element_by_xpath('//*[@title="Sent Items"]')
sent_emails_button.click()
time.sleep(1)
sent_email_titles = browser.find_elements_by_class_name('RKJYnFQ991LYsw_styUw')
assert not any([title.text == email_subject for title in sent_email_titles])
logging.info("E-mail hasn't been sent yet, and no e-mail with our test title was found.")

# Create new e-mail
new_mail_button = browser.find_element_by_class_name('_39t1Yy85WX6tG-kM3-jR-t')
new_mail_button.click()
time.sleep(1)

recipient_element = browser.find_element_by_class_name('pickerInput_269bfa71')
recipient_element.send_keys(recipient)
time.sleep(0.5)
suggestion_button = browser.find_element_by_id('sug-0')
suggestion_button.click()

subject_element = browser.find_element_by_id('subjectLine0')
subject_element.send_keys(email_subject)

# Attach file
body_element = browser.find_element_by_class_name('_1iWL2ddLCtiEp9P-UVh8nV')
body_element.send_keys(file_to_send)
time.sleep(1)

# Send e-mail
send_button = browser.find_element_by_xpath('//*[@title="Send"]')
send_button.click()
time.sleep(1)

# Validate that the file was sent
sent_email_titles = browser.find_elements_by_class_name('RKJYnFQ991LYsw_styUw')
assert any([title.text == email_subject for title in sent_email_titles])
logging.info("Sent e-mail has been found! Tests passed with success.")
