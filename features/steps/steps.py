from behave import *
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

email_subject = "A friendly bug."
reply_email_subject = "Send me bugs."
timeout_seconds = 10
browser = webdriver.Chrome()


@given('I am a user with a valid outlook email address')
def step_impl(context):
    assert username and password


@given('I am logged in to my email')
def step_impl(context):
    # Log in to the sender's account
    goto_inbox()

    try:
        # We might need to log in
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
    except NoSuchElementException:
        # If we couldn't find an element, it could be because we're already logged in.
        # If we see the "Inbox", we are already logged in.
        inbox_element = browser.find_element_by_xpath("//*[contains(text(),'Inbox')]")


@given('I have an e-mail to reply to')
def step_impl(context):
    # Send an e-mail to yourself to have an e-mail to reply to.
    create_new_email()
    context.email_subject = reply_email_subject
    enter_subject(reply_email_subject)
    add_recipient(username)
    send_email()

    # Wait for the e-mail we sent ourselves to be visible.
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, f"//div[contains(@aria-label, '{reply_email_subject}')]")
        )
    )


@given('I want to send a new message to {address}')
def step_impl(context, address):
    context.email_subject = email_subject
    goto_sent_items()

    sent_email_title = browser.find_elements_by_xpath(f"//*[contains(text(),'{email_subject}')]")

    # Verify that no such email exists yet
    assert not sent_email_title

    # Create new e-mail
    create_new_email()

    # Add recipient
    add_recipient(address)


@given('I want to send a new message')
def step_impl(context):
    context.email_subject = email_subject

    # Create new e-mail
    create_new_email()


@when('I do not have a recipient')
def step_impl(context):
    pass


@when('the subject to my e-mail is: A friendly bug.')
def step_impl(context):
    enter_subject(context.email_subject)


@when('the image {attachment} is attached in the e-mail body')
def step_impl(context, attachment):
    attach_file(attachment)


@when('I reply to the e-mail')
def step_impl(context):
    browser.find_element_by_xpath(f"//div[contains(@aria-label,'{context.email_subject}')]").click()

    # Wait for reply button to appear
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, "//div[contains(@aria-label, 'Content pane')]//button[@aria-label='Reply']")
        )
    )
    browser.find_element_by_xpath("//div[contains(@aria-label,'Content pane')]//button[@aria-label='Reply']").click()
    browser.find_element_by_xpath("//label[contains(text(),'To:')]").click()


@when('I include {address} in the reply')
def step_impl(context, address):
    add_recipient(address)


@when('I send my e-mail')
def step_impl(context):
    send_email()


@then('an email with {attachment} attached for {address} should appear in my Sent folder')
def step_impl(context, attachment, address):
    goto_sent_items()

    # Validate that the file was sent
    email_card_ref = f"//div[contains(@aria-label, 'Has attachments {context.email_subject}')]"

    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, email_card_ref)
        )
    )
    # Click the sent e-mail
    browser.find_element_by_xpath(email_card_ref).click()
    
    attachment_element = browser.find_element_by_xpath(f"//div[@aria-label='{attachment} Open']")

    assert attachment_element is not None

    remove_sent_email(context.email_subject)

    cleanup_inbox(context.email_subject)


@then('the system warns me to enter at least one recipient')
def step_impl(context):
    error_badge = browser.find_element_by_xpath("//i[@data-icon-name='ErrorBadge']")
    error_message = browser.find_element_by_xpath("//span[contains(text(),'This message must have at least one recipient.')]")
    assert error_badge and error_message

    browser.find_element_by_xpath("//button[@aria-label='Discard']").click()
    browser.find_element_by_id('ok-1').click()


"""
Helper functions:
Below are helper functions re-used across the various tests.
"""
def remove_sent_email(subject):
    email_card_ref = f"//div[contains(@aria-label, 'Has attachments {subject}')]"
    delete_button_ref = f"//div[contains(@aria-label, 'Has attachments {subject}')]//button[@title='Delete']"

    email_card = browser.find_element_by_xpath(email_card_ref)

    # Delete sent email to restore initial conditions
    hoverover = ActionChains(browser).move_to_element(email_card).click().perform()
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, delete_button_ref)
        )
    )

    browser.find_element_by_xpath(delete_button_ref).click()
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.invisibility_of_element_located( 
            (By.XPATH, email_card_ref)
        )
    )


def cleanup_inbox(subject):
    goto_inbox()
    # We attempt to clean up the inbox.
    # In the alternate flow, we create a temporary e-mail to reply to.
    try:
        remove_sent_email(subject)
    except NoSuchElementException:
        pass




def log_out():
    # Log out
    browser.find_element_by_id("O365_MainLink_Me").click()
    browser.find_element_by_id('meControlSignoutLink').click()


def create_new_email():
    # Create new e-mail
    new_mail_button = browser.find_element_by_class_name('_39t1Yy85WX6tG-kM3-jR-t')
    new_mail_button.click()
    # Wait until we see the new message form
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.CLASS_NAME, 'pickerInput_269bfa71')
        )
    )


def enter_subject(subject):
    subject_element = browser.find_element_by_id('subjectLine0')
    subject_element.send_keys(subject)


def add_recipient(recipient):
    recipient_element = browser.find_element_by_class_name('pickerInput_269bfa71')
    recipient_element.send_keys(recipient)

    # Wait until we see the user suggestion picker
    try:
        WebDriverWait(browser, timeout_seconds).until( 
            expected_conditions.presence_of_element_located( 
                (By.ID, 'sug-0')
            )
        )

        suggestion_button = browser.find_element_by_id('sug-0')
        suggestion_button.click()
    except TimeoutException:
        # This just means we couldn't get a good suggestion by outlook
        # for this recipient. We can just send the e-mail regardless.
        pass


def attach_file(filename):
    # Attach file
    file_to_send = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                filename)
    body_element = browser.find_element_by_xpath("//input[@type='file' and @accept='*/*']")
    #'_1iWL2ddLCtiEp9P-UVh8nV'
    body_element.send_keys(file_to_send)

    # Wait for image to be fully uploaded
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, f"//div[@aria-label='Content pane']//div[contains(@aria-label, '{filename}')]")
        )
    )
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.XPATH, f"//div[@aria-label='Content pane']//img[contains(@src, 'https://attachments.office.net/owa/{username}')]")
        )
    )


def goto_sent_items():
    sent_emails_button = browser.find_element_by_xpath('//*[@title="Sent Items"]')
    sent_emails_button.click()

    # Wait until we see "sent" messages
    WebDriverWait(browser, timeout_seconds).until( 
        expected_conditions.presence_of_element_located( 
            (By.CLASS_NAME, 'RKJYnFQ991LYsw_styUw')
        )
    )


def goto_inbox():
    browser.get('https://outlook.office.com/mail/inbox')
    try:
        WebDriverWait(browser, 3).until(
            expected_conditions.alert_is_present()
        )

        alert = browser.switch_to.alert
        alert.accept()
    except TimeoutException:
        pass


def send_email():
    # Send e-mail
    send_button = browser.find_element_by_xpath('//*[@title="Send"]')
    send_button.click()
