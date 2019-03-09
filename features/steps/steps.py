from behave import *
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import time

# Get the variables the user must set for the test to run.
# Warn the user if these are not set as the test can not run.
username = os.environ.get("email_username", "")
password = os.environ.get("email_password", "")

# Three different recipients + three different attachments = six tests with different recipients & attachments.
recipients = ["andrei.ungur@mail.mcgill.ca", "suleman.malik@mail.mcgill.ca", "andreiskate2@hotmail.com"]
files = ["friendlybug.gif", "instructions.pdf", "bugriver.html"]

email_subject = "Hello from Selenium!"
timeout_seconds = 10
browser = webdriver.Chrome()


@given('I am a user with a valid outlook email address')
def step_impl(context):
    assert username and password


@given('I am logged in to my email')
def step_impl(context):
    # Log in to the sender's account
    browser.get('https://outlook.office.com/mail/inbox')

    email_element = browser.find_element_by_name('loginfmt')
    email_element.send_keys(username)

    continue_button = browser.find_element_by_id('idSIButton9')
    continue_button.click()

    # Wait for the password input to appear
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.ID, 'passwordInput')
        )
    )

    password_element = browser.find_element_by_id('passwordInput')
    password_element.send_keys(password)

    login_button = browser.find_element_by_id('submitButton')
    login_button.click()
    # Wait for the screen to ask if we want to save our login info
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.ID, 'idBtn_Back')
        )
    )

    dont_save_login_button = browser.find_element_by_id('idBtn_Back')
    dont_save_login_button.click()

    # Wait until we're successfully logged in
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, "//*[contains(text(),'Inbox')]")
        )
    )
    # If by this point we didn't get a timeout, the login is successful!


@when('I press “new message”')
def step_impl(context):
    sent_emails_button = browser.find_element_by_xpath('//*[@title="Sent Items"]')
    sent_emails_button.click()

    # Wait until we see "sent" messages
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.CLASS_NAME, 'RKJYnFQ991LYsw_styUw')
        )
    )

    sent_email_title = browser.find_elements_by_xpath(f"//*[contains(text(),'{email_subject}')]")

    # Verify that no such email exists yet
    assert not sent_email_title

    # Create new e-mail
    new_mail_button = browser.find_element_by_class_name('_39t1Yy85WX6tG-kM3-jR-t')
    new_mail_button.click()
    # Wait until we see the new message form
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.CLASS_NAME, 'pickerInput_269bfa71')
        )
    )


@when('I enter a recipient in the “To” input field')
def step_impl(context):
    recipient_element = browser.find_element_by_class_name('pickerInput_269bfa71')
    recipient_element.send_keys(recipients[0])

    # Wait until we see the user suggestion picker
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.ID, 'sug-0')
        )
    )

    suggestion_button = browser.find_element_by_id('sug-0')
    suggestion_button.click()


@when('I enter a subject')
def step_impl(context):
    subject_element = browser.find_element_by_id('subjectLine0')
    subject_element.send_keys(email_subject)


@when('I add an image to the e-mail body')
def step_impl(context):
    # Attach file
    file_to_send = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                files[0])
    body_element = browser.find_element_by_class_name('_1iWL2ddLCtiEp9P-UVh8nV')
    body_element.send_keys(file_to_send)

    # Wait for image to be fully uploaded
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, f"//div[@aria-label='{files[0]} Open']")
        )
    )


@when('I press “Send”')
def step_impl(context):
    # Send e-mail
    send_button = browser.find_element_by_xpath('//*[@title="Send"]')
    send_button.click()

    # Wait until e-mail is fully sent
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, "//*[contains(text(),'Select an item to read')]")
        )
    )


@then('the email should send to the specified recipient')
def step_impl(context):
    # Validate that the file was sent
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, f"//*[contains(text(),'{email_subject}')]")
        )
    )
    # Click the sent e-mail
    browser.find_element_by_xpath(f"//div[@aria-label='Has attachments {email_subject}']").click()
    
    attachment = browser.find_element_by_xpath(f"//div[@aria-label='{files[0]} Open']")

    assert attachment is not None
    delete_sent_email()
    browser.close()


def delete_sent_email():
    email_card = browser.find_element_by_xpath(f"//div[@aria-label='Has attachments {email_subject}']")
    hoverover = ActionChains(browser).move_to_element(email_card).click().perform()
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, f"//Button[@title='Delete']")
        )
    )
    browser.find_element_by_xpath("//Button[@title='Delete']").click()
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.invisibility_of_element_located( 
            (By.XPATH, f"//div[@aria-label='Has attachments {email_subject}']")
        )
    )